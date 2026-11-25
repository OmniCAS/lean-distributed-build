import E1.Formalism.HermitianCurvature.BlockKernelPropertiesOfSteps
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.ColumnOperationTripleForm
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.FirstKernelPropertiesOfHypotheses
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.KernelNonzeroModulusDeterminantEq
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.KernelQuotientFinite
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.LatticeAverageIdentity
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.TripleForm

set_option Elab.async false

namespace E1N.M635
def val : Nat := E1N.M451.val % 7 + E1N.M530.val % 7 + E1N.M556.val % 7 + E1N.M579.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M635
