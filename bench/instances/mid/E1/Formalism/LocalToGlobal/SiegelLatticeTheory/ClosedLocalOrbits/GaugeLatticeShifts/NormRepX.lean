import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedLocalOrbits.GaugeLatticeShifts.PairValPf
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.ClosedVolumeStatements.GenericRatioOfBoundHolds
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.NormRepresentationLift.NormRepStepOfTrace
import E1.Formalism.PeriodIntegrals.UnitaryGroupMassFormula.NormRepresentationLift.StarSqrtMinusD

set_option Elab.async false

namespace E1N.M1032
def val : Nat := E1N.M1035.val % 7 + E1N.M1106.val % 7 + E1N.M1871.val % 7 + E1N.M1874.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M1032
