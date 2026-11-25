import E1.Formalism.HermitianCurvature.BlockKernelPropertiesOfSteps
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.AddedBlockKernelSupport
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.CharacterOrthogonalityDual
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.FirstKernelExplicitFormula
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.FirstKernelPropertiesOfHypotheses
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.KernelNonzeroModulusDeterminantEq
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.KernelQuotientFinite

set_option Elab.async false

namespace E1N.M555
def val : Nat := E1N.M451.val % 7 + E1N.M454.val % 7 + E1N.M523.val % 7 + E1N.M554.val % 7 + 1
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
end E1N.M555
