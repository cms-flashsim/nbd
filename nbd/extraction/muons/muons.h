// utilities for MUON
#ifndef UTILS_MUON_H
#define UTILS_MUON_H

auto MDeltaPhi(ROOT::VecOps::RVec<float> &Phi1,
               ROOT::VecOps::RVec<float> &Phi2) {
  auto size = Phi1.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size);
  for (size_t i = 0; i < size; i++) {
    Double_t dphi = TVector2::Phi_mpi_pi(Phi1[i] - Phi2[i]);
    dphis.emplace_back(dphi);
  }
  return dphis;
}
auto Mclosest_jet_dr(ROOT::VecOps::RVec<float> &etaj,
                     ROOT::VecOps::RVec<float> &phij,
                     ROOT::VecOps::RVec<float> &etam,
                     ROOT::VecOps::RVec<float> &phim) {

  auto size_outer = etam.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> distances;
  distances.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    distances.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etam[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phim[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
      }
    }
    if (closest < 0.4) {
      distances[i] = closest;
    }
  }
  return distances;
}
auto Mclosest_jet_mass(ROOT::VecOps::RVec<float> &etaj,
                       ROOT::VecOps::RVec<float> &phij,
                       ROOT::VecOps::RVec<float> &etam,
                       ROOT::VecOps::RVec<float> &phim,
                       ROOT::VecOps::RVec<float> &massj) {

  auto size_outer = etam.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> masses;
  masses.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    masses.emplace_back(0.0);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etam[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phim[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        masses[i] = massj[j];
      }
    }
  }
  return masses;
}
auto Mclosest_jet_pt(ROOT::VecOps::RVec<float> &etaj,
                     ROOT::VecOps::RVec<float> &phij,
                     ROOT::VecOps::RVec<float> &etam,
                     ROOT::VecOps::RVec<float> &phim,
                     ROOT::VecOps::RVec<float> &ptj) {

  auto size_outer = etam.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> pts;
  pts.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    pts.emplace_back(0.0);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etam[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phim[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        pts[i] = ptj[j];
      }
    }
  }
  return pts;
}
auto Mclosest_jet_deta(ROOT::VecOps::RVec<float> &etaj,
                       ROOT::VecOps::RVec<float> &phij,
                       ROOT::VecOps::RVec<float> &etam,
                       ROOT::VecOps::RVec<float> &phim) {

  auto size_outer = etam.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> detas;
  detas.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    detas.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etam[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phim[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        detas[i] = deta;
      }
    }
  }
  return detas;
}
auto Mclosest_jet_dphi(ROOT::VecOps::RVec<float> &etaj,
                       ROOT::VecOps::RVec<float> &phij,
                       ROOT::VecOps::RVec<float> &etam,
                       ROOT::VecOps::RVec<float> &phim) {

  auto size_outer = etam.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    dphis.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etam[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phim[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        dphis[i] = dphi;
      }
    }
  }
  return dphis;
}
auto MBitwiseDecoder(ROOT::VecOps::RVec<int> &ints, int bit) {
  auto size = ints.size();
  ROOT::VecOps::RVec<float> bits;
  bits.reserve(size);
  int num = pow(2, (bit));
  for (size_t i = 0; i < size; i++) {
    Double_t bAND = ints[i] & num;
    if (bAND == num) {
      bits.emplace_back(1);
    } else {
      bits.emplace_back(0);
    }
  }
  return bits;
}

auto muons_per_event(ROOT::VecOps::RVec<int> &MGM) {
  int size = MGM.size();
  return size;
}

auto Mcharge(ROOT::VecOps::RVec<int> &pdgId) {
  auto size = pdgId.size();
  ROOT::VecOps::RVec<float> charge;
  charge.reserve(size);
  for (size_t i = 0; i < size; i++) {
    if (pdgId[i] == -13)
      charge.emplace_back(-1);
    else
      charge.emplace_back(+1);
  }
  return charge;
}

#endif