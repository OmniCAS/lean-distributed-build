import E1.Formalism.SatakeDualWeyl.AdelicIwasawaHecke.Ipindep
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.ChainScalar
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.ClassRepsDefinite
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.DetSwap
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.EigenSwap
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.FFPlancherel
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.GaussOp
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.LatLiftIndep
import E1.Formalism.ThetaLiftIndependence.ThetaOrbitSums.OrbitSum

set_option Elab.async false

namespace E1N.M2622
def val : Nat := E1N.M2198.val % 7 + E1N.M2624.val % 7 + E1N.M2625.val % 7 + E1N.M2626.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
end E1N.M2622
