import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.AntidiagMulDiagonal
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.BudgetLiftSquareRoot
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.DiagonalTopBlock
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.GramConjugationNorm
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.OffDiagonalSchurComplement
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.PointSetConstantMembership
import E1.Formalism.HermitianCurvature.StatementTA

set_option Elab.async false

namespace E1N.M604
def val : Nat := E1N.M462.val % 7 + E1N.M520.val % 7 + E1N.M541.val % 7 + E1N.M562.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M604
