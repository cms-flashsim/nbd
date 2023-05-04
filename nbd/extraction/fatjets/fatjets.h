#ifndef UTILS_FATJETS
#define UTILS_FATJETS

auto count_nHadrons(ROOT::VecOps::RVec<float> &genh_eta,
                    ROOT::VecOps::RVec<float> &genh_phi,
                    ROOT::VecOps::RVec<float> &AK8_eta,
                    ROOT::VecOps::RVec<float> &AK8_phi) {

  /* Calculates the DeltaR from the closest muon object,
          if none present within 0.4, sets DR to 0.4
  */

  auto size_outer = AK8_eta.size();
  auto size_inner = genh_eta.size();
  std::cout << "size_outer: " << size_outer << std::endl;
  std::cout << "size_inner: " << size_inner << std::endl;
  ROOT::VecOps::RVec<int> count_h;
  count_h.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    count_h.emplace_back(0);
    if (size_inner == 0 | size_outer == 0) continue;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = genh_eta[i] - AK8_eta[j];
      Double_t dphi = TVector2::Phi_mpi_pi(genh_phi[i] - AK8_phi[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if (dr < 0.8)
        count_h[i] += 1;
    }
  }
  return count_h;
}

#endif