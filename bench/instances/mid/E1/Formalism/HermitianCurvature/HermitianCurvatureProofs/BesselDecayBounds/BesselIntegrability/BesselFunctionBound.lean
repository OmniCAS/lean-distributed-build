import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.BesselIntegrability.BesselIntegralConvergenceOfGrowth
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.BesselIntegrability.DoubleCosetDecomposition
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.BesselIntegrability.IntegrableGNRpowOfLintegralLtTop
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.HaarCompactGrowth.GrowthSphericalBound
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.SchurDecayBounds.BeBesselOf
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.SchurDecayBounds.NormIdFixM
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BesselDecayBounds.SchurDecayBounds.SchurH

set_option Elab.async false

namespace E1N.M464
def val : Nat := E1N.M465.val % 7 + E1N.M466.val % 7 + E1N.M468.val % 7 + E1N.M494.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M464
