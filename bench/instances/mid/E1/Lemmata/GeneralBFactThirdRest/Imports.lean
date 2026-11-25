import E1.Formalism.CoboundaryTransfers.Statement
import E1.Formalism.FrobeniusOrbits.DiscrMaximalRealCyclotomic
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.RealCyclotomicSubfield
import E1.Formalism.FrobeniusOrbits.HostDiffSupport
import E1.Formalism.FrobeniusOrbits.HostOrbitCountSg
import E1.Formalism.FrobeniusOrbits.HostOrbitsPlaces
import E1.Formalism.FrobeniusOrbits.HostThickExists
import E1.Formalism.FrobeniusOrbits.Statement
import E1.Formalism.HermitianLattices.StatementLat
import E1.Formalism.LocalRingCardinality.DataArith
import E1.Formalism.LocalRingCardinality.DataCD
import E1.Formalism.LocalRingCardinality.DataCoeff
import E1.Formalism.LocalRingCardinality.DataKernels
import E1.Formalism.LocalRingCardinality.DataRows
import E1.Formalism.LocalRingCardinality.DataSpaces
import E1.Formalism.LocalRingCardinality.Params
import E1.Formalism.SharpRestriction.CuspSpanNormBounds.DataS
import E1.Formalism.SharpRestriction.CuspSpanNormBounds.SArith
import E1.Formalism.SharpRestriction.GrowthBounds.DataG
import E1.Formalism.SharpRestriction.RamificationFrobenius.TotientGaloisClasses.ConjEMemHostFIff
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.ConjEqInvOfPowEqOne
import E1.Formalism.TameInertiaTowers.CentralOrderTwo.Galois
import E1.Formalism.TameInertiaTowers.FinalGroup

set_option Elab.async false

namespace E1N.M2698
def val : Nat := E1N.M66.val % 7 + E1N.M200.val % 7 + E1N.M220.val % 7 + E1N.M226.val % 7 + 1
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
end E1N.M2698
