import E1.Formalism.HyperbolicPlaceProducts.Statement
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.CardEqCardRangeNsmulMulCardKer
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.CountO
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.DedekindLFunctions
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.OmegaPow
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.SesquilinearDeterminantHolds
import E1.Formalism.HyperbolicPlaceProducts.SubgroupIndexCounts.SubgroupCount

set_option Elab.async false

namespace E1N.M744
def val : Nat := E1N.M745.val % 7 + E1N.M747.val % 7 + E1N.M748.val % 7 + E1N.M749.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M744
