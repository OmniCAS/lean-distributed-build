import Syn.M979
import Syn.M1744

namespace Syn.M1760
def val : Nat := Syn.M979.val % 7 + Syn.M1744.val % 7 + 1
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
theorem w12 (a b : Nat) : a + b + 12 = b + a + 12 := by omega
theorem w13 (a b : Nat) : a + b + 13 = b + a + 13 := by omega
theorem w14 (a b : Nat) : a + b + 14 = b + a + 14 := by omega
theorem w15 (a b : Nat) : a + b + 15 = b + a + 15 := by omega
theorem w16 (a b : Nat) : a + b + 16 = b + a + 16 := by omega
theorem w17 (a b : Nat) : a + b + 17 = b + a + 17 := by omega
theorem w18 (a b : Nat) : a + b + 18 = b + a + 18 := by omega
theorem w19 (a b : Nat) : a + b + 19 = b + a + 19 := by omega
theorem w20 (a b : Nat) : a + b + 20 = b + a + 20 := by omega
theorem w21 (a b : Nat) : a + b + 21 = b + a + 21 := by omega
theorem w22 (a b : Nat) : a + b + 22 = b + a + 22 := by omega
theorem warned (h : 1 = 1) : True := trivial
end Syn.M1760
