import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.CardExtendedGaloisGroup
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.CardTrivialFirstComponent
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.ConjReal
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.CoprimeTwoPow
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.Decomp
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.DiscrB
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.DiscriminantRealSubfield
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.EqZeroOfNegEq
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.ExistsOpenNormalOrderOf
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.FrobMulInertia
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.Galois
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.Inertia
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.MuCardLeTwo
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.NcardEqTwoIff
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.OrbitSg
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.Orbits
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.OrdUnimod
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.OrderOfSignGroupDvdTwo
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.Principal
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.RealCyclotomicSubfield
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.SplitK
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.ThickExists
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.ThickFrames
import E1.Formalism.FrobeniusOrbits.FrobeniusOrbitsProofs.ThickOrbit
import E1.Formalism.FrobeniusOrbits.RealSubfieldLeCompositum

set_option Elab.async false

namespace E1N.M225
def val : Nat := E1N.M201.val % 7 + E1N.M202.val % 7 + E1N.M203.val % 7 + E1N.M204.val % 7 + 1
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
end E1N.M225
