import E1.Development.AbelianVarietyTheory.Proofs.CuspFormEvaluations.ExistsFaithfullyFlatRoots
import E1.Formalism.LocalToGlobal.ProjectiveLattices.ThGerm
import E1.Formalism.LocalToGlobal.ProjectiveLattices.ThShort
import E1.ReciprocityTheory.ReductiveGroups.ArithmeticGeometry.BirationalGeometry.ToroidalCompactification.VtUniq
import E1.ReciprocityTheory.ReductiveGroups.ArithmeticGeometry.ExtensionDescent.SecBaseChangeAnySt

set_option Elab.async false

namespace E1N.M611
def val : Nat := E1N.M610.val % 7 + E1N.M3043.val % 7 + E1N.M3045.val % 7 + E1N.M3906.val % 7 + 1
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
theorem w11 (a b : Nat) : a + b + 11 = b + a + 11 := by omega
end E1N.M611
