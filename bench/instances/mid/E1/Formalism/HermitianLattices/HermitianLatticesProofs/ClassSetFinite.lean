import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ClassSetAssembly
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.FinIntermediate
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusCovolBound
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusScale
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.IsomOfTrace
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ShortVectors
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.TraceReal

set_option Elab.async false

namespace E1N.M707
def val : Nat := E1N.M706.val % 7 + E1N.M712.val % 7 + E1N.M715.val % 7 + E1N.M716.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M707
