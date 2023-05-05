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

#endif