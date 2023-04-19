// utilities for JETS
#ifndef UTILS_JET_H
#define UTILS_JET_H

auto DeltaPhi(ROOT::VecOps::RVec<float> &Phi1,
              ROOT::VecOps::RVec<float> &Phi2) {

  /* Calculates the DeltaPhi between two RVecs
   */

  auto size = Phi1.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size);
  for (size_t i = 0; i < size; i++) {
    Double_t dphi = TVector2::Phi_mpi_pi(Phi1[i] - Phi2[i]);
    dphis.emplace_back(dphi);
  }
  return dphis;
}

auto closest_muon_dr(ROOT::VecOps::RVec<float> &etaj,
                     ROOT::VecOps::RVec<float> &phij,
                     ROOT::VecOps::RVec<float> &etam,
                     ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaR from the closest muon object,
          if none present within 0.4, sets DR to 0.4
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> distances;
  distances.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    distances.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
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

auto closest_muon_pt(ROOT::VecOps::RVec<float> &etaj,
                     ROOT::VecOps::RVec<float> &phij,
                     ROOT::VecOps::RVec<float> &etam,
                     ROOT::VecOps::RVec<float> &phim,
                     ROOT::VecOps::RVec<float> &ptm) {

  /* Calculates the pt of the closest muon object,
          if none present within 0.4, sets DR to 0.4 and pt to 0 GeV
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> pts;
  pts.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    pts.emplace_back(0.0);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        pts[i] = ptm[j];
      }
    }
  }
  return pts;
}

auto closest_muon_deta(ROOT::VecOps::RVec<float> &etaj,
                       ROOT::VecOps::RVec<float> &phij,
                       ROOT::VecOps::RVec<float> &etam,
                       ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaEta of the closest muon object,
          if none present within 0.4, sets DR to 0.4 and DeltaEta to 0.5
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> detas;
  detas.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    detas.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        detas[i] = deta;
      }
    }
  }
  return detas;
}

auto closest_muon_dphi(ROOT::VecOps::RVec<float> &etaj,
                       ROOT::VecOps::RVec<float> &phij,
                       ROOT::VecOps::RVec<float> &etam,
                       ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaPhi of the closest muon object,
          if none present within 0.4, sets DR to 0.4 and DeltaPhi to 0.5
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    dphis.emplace_back(0.5);
    float closest = 0.4;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        dphis[i] = dphi;
      }
    }
  }
  return dphis;
}

auto second_muon_dr(ROOT::VecOps::RVec<float> &etaj,
                    ROOT::VecOps::RVec<float> &phij,
                    ROOT::VecOps::RVec<float> &etam,
                    ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaR from the second closest muon object,
          if none present within 0.4, sets DR to 0.4
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> distances;
  distances.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    distances.emplace_back(0.5);
    float closest = 0.4;
    float second_closest = 0.5;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        second_closest = closest;
        closest = dr;
      }
    }
    if (second_closest < 0.4) {
      distances[i] = second_closest;
    }
  }
  return distances;
}

auto second_muon_pt(ROOT::VecOps::RVec<float> &etaj,
                    ROOT::VecOps::RVec<float> &phij,
                    ROOT::VecOps::RVec<float> &etam,
                    ROOT::VecOps::RVec<float> &phim,
                    ROOT::VecOps::RVec<float> &ptm) {

  /* Calculates the pt of the second closest muon object,
          if none present within 0.4, sets DR to 0.4 and pt to 0 GeV
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> pts;
  pts.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    pts.emplace_back(0.0);
    float closest = 0.4;
    float second_closest = 0.5;
    float closest_pt = 0.0;
    float second_pt = 0.0;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        second_closest = closest;
        second_pt = closest_pt;
        closest = dr;
        closest_pt = ptm[j];
      }
      if (second_closest < 0.4) {
        pts[i] = second_pt;
      }
    }
  }
  return pts;
}

auto second_muon_deta(ROOT::VecOps::RVec<float> &etaj,
                      ROOT::VecOps::RVec<float> &phij,
                      ROOT::VecOps::RVec<float> &etam,
                      ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaEta of the second closest muon object,
          if none present within 0.4, sets DR to 0.4 and DeltaEta to 0.5
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> detas;
  detas.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    detas.emplace_back(0.5);
    float closest = 0.4;
    float second_closest = 0.5;
    float closest_deta = 0.0;
    float second_deta = 0.0;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        second_closest = closest;
        second_deta = closest_deta;
        closest = dr;
        closest_deta = deta;
      }
      if (second_closest < 0.4) {
        detas[i] = second_deta;
      }
    }
  }
  return detas;
}

auto second_muon_dphi(ROOT::VecOps::RVec<float> &etaj,
                      ROOT::VecOps::RVec<float> &phij,
                      ROOT::VecOps::RVec<float> &etam,
                      ROOT::VecOps::RVec<float> &phim) {

  /* Calculates the DeltaPhi of the second closest muon object,
          if none present within 0.4, sets DR to 0.4 and DeltaPhi to 0.5
  */

  auto size_outer = etaj.size();
  auto size_inner = etam.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    dphis.emplace_back(0.5);
    float closest = 0.4;
    float second_closest = 0.5;
    float closest_dphi = 0.0;
    float second_dphi = 0.0;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etaj[i] - etam[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phij[i] - phim[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        second_closest = closest;
        second_dphi = closest_dphi;
        closest = dr;
        closest_dphi = dphi;
      }
      if (second_closest < 0.4) {
        dphis[i] = second_dphi;
      }
    }
  }
  return dphis;
}

#endif