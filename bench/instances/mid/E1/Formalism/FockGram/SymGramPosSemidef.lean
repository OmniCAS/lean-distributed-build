import E1.Formalism.FockGram.FockGramProofs.CovolGram
import E1.Formalism.FockGram.FockGramProofs.DetSymPow
import E1.Formalism.FockGram.FockGramProofs.FockHerm
import E1.Formalism.FockGram.FockGramProofs.FockPerm
import E1.Formalism.FockGram.FockGramProofs.FockSesq
import E1.Formalism.FockGram.FockGramProofs.HermDualOf
import E1.Formalism.FockGram.FockGramProofs.HermitianTensorMulHermitian
import E1.Formalism.FockGram.FockGramProofs.SubIndexNorm
import E1.Formalism.FockGram.StatementSymPos

set_option Elab.async false

namespace E1N.M168
def val : Nat := E1N.M155.val % 7 + E1N.M156.val % 7 + E1N.M157.val % 7 + E1N.M158.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M168
