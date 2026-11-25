import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.CovolEqCovolume
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.CovolEqGram
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.CovolPos
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.DegQuot
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.FiniteSaturated
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.GramDetLe
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.MuMaxAttained
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.MuMaxLeMin
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.OrthSum
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.SaturationProperties
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.ShortVector
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.SlopeInequality
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.SlopeLeMuMaxOf
import E1.Formalism.LatticeSlopes.LatticeSlopesProofs.SlopesBdd

set_option Elab.async false

namespace E1N.M773
def val : Nat := E1N.M774.val % 7 + E1N.M775.val % 7 + E1N.M776.val % 7 + E1N.M777.val % 7 + 1
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
end E1N.M773
