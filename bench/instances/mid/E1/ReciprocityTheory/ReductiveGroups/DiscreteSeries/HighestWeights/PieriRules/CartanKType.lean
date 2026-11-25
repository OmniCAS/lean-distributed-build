import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.ContinuousRepresentations.URepCompRed
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.CountNotTwoOfFinrankLeOne
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.ExpEntryHasDerivAt
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.InnerLowerSelf
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.LowComp
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.PPlusPWtInjective
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.PrhoEntryHasDerivAt
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.StdExpEntryHasDerivAt
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.TensHW
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.TensRepB
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.WeylPos
import E1.ReciprocityTheory.ReductiveGroups.DiscreteSeries.HighestWeights.PieriRules.WeylSum

set_option Elab.async false

namespace E1N.M2964
def val : Nat := E1N.M2936.val % 7 + E1N.M2965.val % 7 + E1N.M2966.val % 7 + E1N.M2967.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M2964
