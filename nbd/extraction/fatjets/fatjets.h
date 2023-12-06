#ifndef UTILS_FATJETS
#define UTILS_FATJETS

auto count_nHadrons(const ROOT::VecOps::RVec<float> &genh_eta,
                    const ROOT::VecOps::RVec<float> &genh_phi,
                    const ROOT::VecOps::RVec<float> &AK8_eta,
                    const ROOT::VecOps::RVec<float> &AK8_phi) {

  /* Calculates the DeltaR from the closest muon object,
          if none present within 0.4, sets DR to 0.4
  */
 // std::co
  auto size_outer = AK8_eta.size();
  auto size_inner = genh_eta.size();
  ROOT::VecOps::RVec<int> count_h (size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    count_h[i] = 0;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = genh_eta[j] - AK8_eta[i];
      Double_t dphi = TVector2::Phi_mpi_pi(genh_phi[j] - AK8_phi[i]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if (dr < 0.8)
        count_h[i] += 1;
    }
  }

  return count_h;
}

ROOT::VecOps::RVec<int> has_H_within_0_8(ROOT::VecOps::RVec<float> &genpart_eta, ROOT::VecOps::RVec<float> &genpart_phi, ROOT::VecOps::RVec<int> &genpart_id, ROOT::VecOps::RVec<float> &genjetAK8_eta, ROOT::VecOps::RVec<float> &genjetAK8_phi)
{

    int genpart_size = genpart_eta.size();
    int genjet_size = genjetAK8_eta.size();

    ROOT::VecOps::RVec<int> is_h_within_0_8(genjet_size);

    for (int i = 0; i < genjet_size; i++)
    {
        float dr_0 = 0.8;
        is_h_within_0_8[i] = 0;

        for (int j = 0; j < genpart_size; j++)
        {
            float dr = delta_R(genjetAK8_eta[i], genjetAK8_phi[i], genpart_eta[j], genpart_phi[j]);
            if (dr < dr_0 && genpart_id[j] ==25)
            is_h_within_0_8[i] = 1;

        }
    }

    return is_h_within_0_8;
}

#endif