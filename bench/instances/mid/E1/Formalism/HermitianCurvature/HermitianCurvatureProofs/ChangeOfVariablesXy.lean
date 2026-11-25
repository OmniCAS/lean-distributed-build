import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.AffineChangeOfVariables
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.CuspidalIrreducibleSubrep
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.EtaleIntegralityFacts
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.FourierUniquenessMirabolic
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.OrbitTailEstimates
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.OrbitalIntegralConvergesAbs
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.PhaseFunctionCriticalPoints
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.PhaseFunctionDerivatives
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.StandardCharacterExists
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.StationaryPhaseEstimates
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.StationaryPhaseModel
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.WeakApproximationGL
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.WhittakerVanishingImpliesZero
import E1.Formalism.HermitianCurvature.HermitianCurvatureProofs.WirtingerIntegrationByParts
import E1.Formalism.HermitianCurvature.StatementG

set_option Elab.async false

namespace E1N.M522
def val : Nat := E1N.M461.val % 7 + E1N.M540.val % 7 + E1N.M548.val % 7 + E1N.M558.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
theorem w4 (a b : Nat) : a + b + 4 = b + a + 4 := by omega
theorem w5 (a b : Nat) : a + b + 5 = b + a + 5 := by omega
theorem w6 (a b : Nat) : a + b + 6 = b + a + 6 := by omega
theorem w7 (a b : Nat) : a + b + 7 = b + a + 7 := by omega
end E1N.M522
