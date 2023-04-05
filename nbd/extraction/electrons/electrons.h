// utilities for electrons
#ifndef UTILS_ELE_H
#define UTILS_ELE_H

auto clean_genjet_mask(ROOT::VecOps::RVec<float> &jet_pt,
                       ROOT::VecOps::RVec<float> &jet_eta,
                       ROOT::VecOps::RVec<float> &jet_phi,
                       ROOT::VecOps::RVec<float> &lep_pt,
                       ROOT::VecOps::RVec<float> &lep_eta,
                       ROOT::VecOps::RVec<float> &lep_phi) {
  /* Mask to remove GenElectrons  and GenMuons from the GenJet collection.*/
  auto lep_size = lep_pt.size();
  auto jet_size = jet_pt.size();

  ROOT::VecOps::RVec<int> clean_jet_mask;
  clean_jet_mask.reserve(jet_size);

  for (size_t i = 0; i < jet_size; i++) {
    clean_jet_mask.push_back(1);
    for (size_t j = 0; j < lep_size; j++) {
      auto dpt = jet_pt[i] - lep_pt[j];
      auto deta = jet_eta[i] - lep_eta[j];
      auto dphi = TVector2::Phi_mpi_pi(jet_phi[i] - lep_phi[j]);
      auto dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if ((dr <= 0.01) && ((dpt / lep_pt[j]) <= 0.001)) {
        clean_jet_mask[i] = 0;
      }
    }
  }
  return clean_jet_mask;
}

auto closest_jet_dr(ROOT::VecOps::RVec<float> &etaj,
                    ROOT::VecOps::RVec<float> &phij,
                    ROOT::VecOps::RVec<float> &etae,
                    ROOT::VecOps::RVec<float> &phie) {
  /* Calculates the DeltaR from the closest Jet object,
          if none present within 10, sets DR to 10
  */
  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> distances;
  distances.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    distances.emplace_back(10);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
      }
    }
    if (closest < 10) {
      distances[i] = closest;
    }
  }
  return distances;
}

auto closest_jet_mass(ROOT::VecOps::RVec<float> &etaj,
                      ROOT::VecOps::RVec<float> &phij,
                      ROOT::VecOps::RVec<float> &etae,
                      ROOT::VecOps::RVec<float> &phie,
                      ROOT::VecOps::RVec<float> &massj) {

  /* Calculates the mass of the closest Jet object,
          if none present within 10, sets mass to 0 GeV
  */

  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> masses;
  masses.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    masses.emplace_back(0.0);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        masses[i] = massj[j];
      }
    }
  }
  return masses;
}

auto closest_jet_pt(ROOT::VecOps::RVec<float> &etaj,
                    ROOT::VecOps::RVec<float> &phij,
                    ROOT::VecOps::RVec<float> &etae,
                    ROOT::VecOps::RVec<float> &phie,
                    ROOT::VecOps::RVec<float> &ptj) {

  /* Calculates the pt of the closest Jet object,
          if none present within 10, sets pt to 0 GeV
  */

  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> pts;
  pts.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    pts.emplace_back(0.0);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        pts[i] = ptj[j];
      }
    }
  }
  return pts;
}

auto closest_jet_deta(ROOT::VecOps::RVec<float> &etaj,
                      ROOT::VecOps::RVec<float> &phij,
                      ROOT::VecOps::RVec<float> &etae,
                      ROOT::VecOps::RVec<float> &phie) {

  /* Calculates the DeltaEta of the closest Jet object,
          if none present within 10, sets DeltaEta to 0.5
  */

  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> detas;
  detas.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    detas.emplace_back(4);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        detas[i] = deta;
      }
    }
  }
  return detas;
}

auto closest_jet_dphi(ROOT::VecOps::RVec<float> &etaj,
                      ROOT::VecOps::RVec<float> &phij,
                      ROOT::VecOps::RVec<float> &etae,
                      ROOT::VecOps::RVec<float> &phie) {

  /* Calculates the DeltaPhi of the closest Jet object,
          if none present within 0.4, sets DR to 0.4 and DeltaPhi to 0.5
  */
  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    dphis.emplace_back(4);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        dphis[i] = dphi;
      }
    }
  }
  return dphis;
}

auto closest_jet_flavour_encoder(ROOT::VecOps::RVec<float> &etaj,
                                 ROOT::VecOps::RVec<float> &phij,
                                 ROOT::VecOps::RVec<float> &etae,
                                 ROOT::VecOps::RVec<float> &phie,
                                 ROOT::VecOps::RVec<int> &fj,
                                 ROOT::VecOps::RVec<int> flavours) {

  /* General function to encode the hadron and parton flavour of the closest Jet
     object. To be used for flavour one-hot encoding for training.
  */

  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  auto n_flavours = flavours.size();
  ROOT::VecOps::RVec<int> fenc;
  fenc.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    fenc.emplace_back(0);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
        for (size_t k = 0; k < n_flavours; k++) {
          if (abs(fj[j]) == flavours[k]) {
            fenc[i] = 1;
          }
        }
      }
    }
  }
  return fenc;
}

auto BitwiseDecoder(ROOT::VecOps::RVec<int> &ints, int bit) {
  /* Utility function for performing bitwise decoding of
          GenPart_statusFlags conditioning variable
  */
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

auto charge(ROOT::VecOps::RVec<int> &pdgId) {
  /* Assigns the correct charge to the electron according to its gen pdg id
   */
  auto size = pdgId.size();
  ROOT::VecOps::RVec<float> charge;
  charge.reserve(size);
  for (size_t i = 0; i < size; i++) {
    if (pdgId[i] == -11)
      charge.emplace_back(+1);
    else
      charge.emplace_back(-1);
  }
  return charge;
}

auto flavour_encoder(ROOT::VecOps::RVec<int> &fj,
                     ROOT::VecOps::RVec<int> flavours) {

  auto size = fj.size();
  auto n_flavours = flavours.size();

  ROOT::VecOps::RVec<int> fenc;
  fenc.reserve(size);

  for (size_t i = 0; i < size; i++) {
    fenc.emplace_back(0);
    for (size_t k = 0; k < n_flavours; k++) {
      if (abs(fj[i]) == flavours[k]) {
        fenc[i] = 1;
      }
    }
  }

  return fenc;
}

#endif