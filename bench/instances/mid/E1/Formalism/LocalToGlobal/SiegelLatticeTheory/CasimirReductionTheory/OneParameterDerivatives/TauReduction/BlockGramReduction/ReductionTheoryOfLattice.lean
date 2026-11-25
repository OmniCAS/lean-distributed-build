import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.ExistsMulMulConjTransposeEqOne
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.FreeQuotientRank
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.Imports
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.KsetInvMem
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.LatticeFinitelyGeneratedOfCommensurable
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.LatticeVectorsBoundedBelow
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.MemIntegersOfMemIntAd
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.PacketConditionsClosed
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.T7
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.BlockGramReduction.ThirdEstimateOfFirstTwo
import E1.Formalism.LocalToGlobal.SiegelLatticeTheory.CasimirReductionTheory.OneParameterDerivatives.TauReduction.ReductionTauOf

set_option Elab.async false

namespace E1N.M972
def val : Nat := E1N.M962.val % 7 + E1N.M963.val % 7 + E1N.M964.val % 7 + E1N.M965.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
end E1N.M972
