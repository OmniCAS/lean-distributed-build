import E1.Formalism.TameInertiaTowers.CentralOrderTwo.Groups
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.MemDecompositionSubgroupIff
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.NegOneNeOneUnitsZmodFour
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.NormalOrderTwoCentral
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.OrderOfThreeUnitsTwoPow
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.TwoAdic

set_option Elab.async false

namespace E1N.M2617
def val : Nat := E1N.M2610.val % 7 + E1N.M2611.val % 7 + E1N.M2612.val % 7 + E1N.M2613.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M2617
