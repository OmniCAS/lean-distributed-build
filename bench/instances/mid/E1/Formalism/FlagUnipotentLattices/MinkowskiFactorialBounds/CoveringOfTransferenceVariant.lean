import E1.Formalism.FlagUnipotentLattices.CardSubmodulesAndLinearEquivBounds
import E1.Formalism.FlagUnipotentLattices.CoveringRadius2
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.LatticeSumTupleOfLatticeSumTuple
import E1.Formalism.FlagUnipotentLattices.MinkowskiFactorialBounds.SumComplexEmbeddingsEqSumInfinitePlace
import E1.Formalism.FlagUnipotentLattices.SubmoduleGeneratorsBound
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.Residue
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.TransferenceCover
import E1.Formalism.PeriodIntegrals.OrbitalBoundsConclusion.TransferenceCoveringDivisor

set_option Elab.async false

namespace E1N.M125
def val : Nat := E1N.M102.val % 7 + E1N.M103.val % 7 + E1N.M137.val % 7 + E1N.M144.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M125
