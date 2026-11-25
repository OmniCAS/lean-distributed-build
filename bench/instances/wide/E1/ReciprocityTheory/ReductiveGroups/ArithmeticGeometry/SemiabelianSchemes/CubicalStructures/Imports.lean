import E1.ReciprocityTheory.ReductiveGroups.ArithmeticGeometry.SemiabelianSchemes.CubicalStructures.CubeSymmetricSwapFirst

set_option Elab.async false

namespace E1N.M4195
def val : Nat := E1N.M4193.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
end E1N.M4195
