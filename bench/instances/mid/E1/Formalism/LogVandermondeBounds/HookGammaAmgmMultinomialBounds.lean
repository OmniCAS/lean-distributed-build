import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.BlockDimensionIdentities
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.CardStabilizerVector
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.FourierIsometryOnNormKernel
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.GammaIntegralPolynomialBound
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.InertPrimeCountBound
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.InterlacingSeparation
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.LengthQuotientLeOfLatticeSandwich
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.LogRatioLowerBoundOfLogVandermondeGap
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.LogRatioUpperBoundOfUpperPlace
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.LogVandermondeVariationUnbounded
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.MulSingleMulApplySelf
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.PrimePowerSubgroupTrivial
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.RamifiedLatticeOperatorIdentity
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.TaylorLogMetric
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.UpperPlaceHolds
import E1.Formalism.LogVandermondeBounds.LogVandermondeProofs.VandNSuccRight

set_option Elab.async false

namespace E1N.M1334
def val : Nat := E1N.M1337.val % 7 + E1N.M1338.val % 7 + E1N.M1339.val % 7 + E1N.M1340.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
end E1N.M1334
