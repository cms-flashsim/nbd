# a class for conditional flow matching methods
# modified to implement  "Flow Matching" (Lipman et al. 2023)
# we also provide a wrapper for the model to only evolve the first part of the input, taking into account the context

import math
import torch
import torch.nn as nn


import torch.nn as nn
import torch


class ModelWrapper(nn.Module):
    def __init__(self, base_model, context_dim=6):
        """
        Wraps a base model to only evolve the first part of the input specifying a certain context using the model.

        Args:
            base_model (nn.Module): The base model to wrap.
        """
        super(ModelWrapper, self).__init__()
        self.base_model = base_model.eval()
        self.context_dim = context_dim

    def forward(self, t, x, **kwargs):
        """
        Forward pass of the wrapped model.

        Args:
            t (torch.Tensor): The time tensor.
            x (torch.Tensor): The input tensor: concatenation of [actual input, context].
            **kwargs: Additional keyword arguments.

        Returns:
            torch.Tensor: The output tensor.
        """
        xt, context = x[:, :-self.context_dim], x[:, -self.context_dim:]
        t_broadcasted = t.expand(x.shape[0], 1)
        # Only evolve xt using the model
        dxt_dt = self.base_model(xt, context=context, flow_time=t_broadcasted)

        # Concatenate the derivatives of xt with zeros for context to keep their values unchanged
        zeros_for_context = torch.zeros_like(context)
        dx_dt = torch.cat([dxt_dt, zeros_for_context], dim=-1)

        return dx_dt

class ModelWrapperNoContext(nn.Module):
    def __init__(self, base_model):
        """
        Wraps a base model to only evolve the first part of the input specifying a certain context using the model.

        Args:
            base_model (nn.Module): The base model to wrap.
        """
        super(ModelWrapperNoContext, self).__init__()
        self.base_model = base_model.eval()

    def forward(self, t, x, **kwargs):
        """
        Forward pass of the wrapped model.

        Args:
            t (torch.Tensor): The time tensor.
            x (torch.Tensor): The input tensor: concatenation of [actual input, context].
            **kwargs: Additional keyword arguments.

        Returns:
            torch.Tensor: The output tensor.
        """
        xt = x
        t_broadcasted = t.expand(x.shape[0], 1)
        # Only evolve xt using the model
        dxt_dt = self.base_model(xt,  flow_time=t_broadcasted)

        return dxt_dt

def pad_t_like_x(t, x):
    """Function to reshape the time vector t by the number of dimensions of x.

    Parameters
    ----------
    x : Tensor, shape (bs, *dim)
        represents the source minibatch
    t : FloatTensor, shape (bs)

    Returns
    -------
    t : Tensor, shape (bs, number of x dimensions)

    Example
    -------
    x: Tensor (bs, C, W, H)
    t: Vector (bs)
    pad_t_like_x(t, x): Tensor (bs, 1, 1, 1)
    """
    if isinstance(t, float):
        return t
    return t.reshape(-1, *([1] * (x.dim() - 1)))


class LipmanOTConditionalFlowMatcher:
    """Base class for conditional flow matching methods. This class implements the independent
    conditional flow matching methods from [1] and serves as a parent class for all other flow
    matching methods.

    It implements:
    - Drawing data from gaussian probability path N(t * x1 + (1 - t) * x0, sigma) function
    - conditional flow matching ut(x1|x0) = x1 - x0
    - score function $\nabla log p_t(x|x0, x1)$
    """

    def __init__(self, sigma: float = 0.0):
        r"""Initialize the ConditionalFlowMatcher class. It requires the hyper-parameter $\sigma$.

        Parameters
        ----------
        sigma : float
        """
        self.sigma = sigma

    def compute_mu_t(self, x0, x1, t):
        """
        Compute the mean of the probability path N(t * x1 + (1 - t) * x0, sigma), see (Eq.14) [1].

        Parameters
        ----------
        x0 : Tensor, shape (bs, *dim)
            represents the source minibatch
        x1 : Tensor, shape (bs, *dim)
            represents the target minibatch
        t : FloatTensor, shape (bs)

        Returns
        -------
        mean mu_t: t * x1 + (1 - t) * x0

        References
        ----------
        [1] Improving and Generalizing Flow-Based Generative Models with minibatch optimal transport, Preprint, Tong et al.
        """
        t = pad_t_like_x(t, x0)
        return t * x1  # t * x1 + (1 - t) * x0

    def compute_sigma_t(self, t):
        """
        Compute the standard deviation of the probability path N(t * x1 + (1 - t) * x0, sigma), see (Eq.14) [1].

        Parameters
        ----------
        t : FloatTensor, shape (bs)

        Returns
        -------
        standard deviation sigma

        References
        ----------
        [1] Improving and Generalizing Flow-Based Generative Models with minibatch optimal transport, Preprint, Tong et al.
        """
        # del t
        return 1 - (1 - self.sigma) * t

    def sample_xt(self, x0, x1, t, epsilon):
        """
        Draw a sample from the probability path N(t * x1 + (1 - t) * x0, sigma), see (Eq.14) [1].

        Parameters
        ----------
        x0 : Tensor, shape (bs, *dim)
            represents the source minibatch
        x1 : Tensor, shape (bs, *dim)
            represents the target minibatch
        t : FloatTensor, shape (bs)
        epsilon : Tensor, shape (bs, *dim)
            noise sample from N(0, 1)

        Returns
        -------
        xt : Tensor, shape (bs, *dim)

        References
        ----------
        [1] Improving and Generalizing Flow-Based Generative Models with minibatch optimal transport, Preprint, Tong et al.
        """
        mu_t = self.compute_mu_t(x0, x1, t)
        sigma_t = self.compute_sigma_t(t)
        sigma_t = pad_t_like_x(sigma_t, x0)
        return mu_t + sigma_t * epsilon

    def compute_conditional_flow(self, x0, x1, t, xt):
        """
        Compute the conditional vector field ut(x1|x0) = x1 - x0, see Eq.(15) [1].

        Parameters
        ----------
        x0 : Tensor, shape (bs, *dim)
            represents the source minibatch
        x1 : Tensor, shape (bs, *dim)
            represents the target minibatch
        t : FloatTensor, shape (bs)
        xt : Tensor, shape (bs, *dim)
            represents the samples drawn from probability path pt

        Returns
        -------
        ut : conditional vector field ut(x1|x0) = x1 - x0

        References
        ----------
        [1] Improving and Generalizing Flow-Based Generative Models with minibatch optimal transport, Preprint, Tong et al.
        """
        # del t, xt
        # print(x1.shape)
        # print(xt.shape)
        # print(t.shape)
        t = pad_t_like_x(t, x0)
        return (x1 - (1 - self.sigma) * xt) / (
            1 - (1 - self.sigma) * t
        )  # .repeat(1,5).view(-1, 5))

    def sample_noise_like(self, x):
        return torch.randn_like(x)

    def sample_location_and_conditional_flow(self, x0, x1, return_noise=False):
        """
        Compute the sample xt (drawn from N(t * x1 + (1 - t) * x0, sigma))
        and the conditional vector field ut(x1|x0) = x1 - x0, see Eq.(15) [1].

        Parameters
        ----------
        x0 : Tensor, shape (bs, *dim)
            represents the source minibatch
        x1 : Tensor, shape (bs, *dim)
            represents the target minibatch
        return_noise : bool
            return the noise sample epsilon


        Returns
        -------
        t : FloatTensor, shape (bs)
        xt : Tensor, shape (bs, *dim)
            represents the samples drawn from probability path pt
        ut : conditional vector field ut(x1|x0) = x1 - x0
        (optionally) eps: Tensor, shape (bs, *dim) such that xt = mu_t + sigma_t * epsilon

        References
        ----------
        [1] Improving and Generalizing Flow-Based Generative Models with minibatch optimal transport, Preprint, Tong et al.
        """
        t = torch.rand(x0.shape[0]).type_as(x0)
        eps = self.sample_noise_like(x0)
        xt = self.sample_xt(x0, x1, t, eps)
        ut = self.compute_conditional_flow(x0, x1, t, xt)
        if return_noise:
            return t, xt, ut, eps
        else:
            return t, xt, ut

    def compute_lambda(self, t):
        """Compute the lambda function, see Eq.(23) [3].

        Parameters
        ----------
        t : FloatTensor, shape (bs)

        Returns
        -------
        lambda : score weighting function

        References
        ----------
        [4] Simulation-free Schrodinger bridges via score and flow matching, Preprint, Tong et al.
        """
        sigma_t = self.compute_sigma_t(t)
        return 2 * sigma_t / (self.sigma**2 + 1e-8)
