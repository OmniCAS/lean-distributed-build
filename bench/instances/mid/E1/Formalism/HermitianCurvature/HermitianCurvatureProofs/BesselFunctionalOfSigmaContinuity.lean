import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.AdmissibleAtomicFormOneReduction
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.BesselIntegrability.BesselFunctionBound
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselNonvanishingFromL2
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.DiscreteSeriesFormOneReduction
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.FdegOfSchur
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.L2NormScaling
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.OrbConvDDOfDecDD
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.PhiRegOf
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.RegularityBundleFromHypotheses
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.ReproducingFormulaReduction
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.VanishingOfL2Equivariant

set_option Elab.async false

namespace E1N.M509
def val : Nat := E1N.M458.val % 7 + E1N.M464.val % 7 + E1N.M511.val % 7 + E1N.M545.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
theorem w8 (a b : Nat) : a + b + 8 = b + a + 8 := by omega
theorem w9 (a b : Nat) : a + b + 9 = b + a + 9 := by omega
theorem w10 (a b : Nat) : a + b + 10 = b + a + 10 := by omega
end E1N.M509
