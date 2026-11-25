import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.MinkowskiSubmoduleShortVector
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.ReductionTheoryOfLattice
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.T8m

set_option Elab.async false

namespace E1N.M971
def val : Nat := E1N.M969.val % 7 + E1N.M972.val % 7 + E1N.M975.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
end E1N.M971
