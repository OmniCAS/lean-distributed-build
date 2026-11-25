import E1.Formalism.GelfandTransference.HadamardGelfand.Transference
import E1.Formalism.LatticeRigidity.HeightMin
import E1.Formalism.LatticeRigidity.HeightMinimum.BlockEquationHolds
import E1.Formalism.LatticeRigidity.HeightMinimum.ChebyshevLeadingCoeffHolds
import E1.Formalism.LatticeRigidity.HeightMinimum.OneLeProdOfInt
import E1.Formalism.LatticeRigidity.HeightMinimum.PackingCountGeometricMean
import E1.Formalism.LatticeRigidity.HeightMinimum.PowFinrankEqZeroOfTracePow
import E1.Formalism.LatticeRigidity.HeightMinimum.SqrtAbsNormLeProd

set_option Elab.async false

namespace E1N.M768
def val : Nat := E1N.M306.val % 7 + E1N.M760.val % 7 + E1N.M761.val % 7 + E1N.M762.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M768
