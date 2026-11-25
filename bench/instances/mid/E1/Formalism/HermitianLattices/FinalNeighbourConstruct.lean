import E1.Formalism.HermitianLattices.DiscrFinite
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.AutFinite
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ClassSetAssembly
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ClassSetFinite
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.DualBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.DualLattice
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.DualOrthSum
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ExampleZ
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.FinIntermediate
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusCovol
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusCovolBound
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.GenusScale
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.IndexBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.IsomAct
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.IsomOfTrace
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.LocBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.LocDual
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.MajBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.MajDual
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.MajLattice
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.NeighbourBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.NeighbourConstruct
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.OpBound
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ShortVectors
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ThetaBasic
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.ThetaSummable
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.TraceReal
import E1.Formalism.HermitianLattices.HermitianLatticesProofs.UnimodUnramUnique
import E1.Formalism.LatticeTheta.ThetaShiftInversion

set_option Elab.async false

namespace E1N.M703
def val : Nat := E1N.M700.val % 7 + E1N.M705.val % 7 + E1N.M706.val % 7 + E1N.M707.val % 7 + 1
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
end E1N.M703
