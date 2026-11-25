import E1.Formalism.SobolevGaussianKernels.GaussianKernelBounds.EichlerEquivalenceHolds
import E1.Formalism.SobolevGaussianKernels.GaussianKernelBounds.HasDerivAtSphereChartLast
import E1.Formalism.SobolevGaussianKernels.GaussianKernelBounds.LfProd
import E1.Formalism.SobolevGaussianKernels.GaussianKernelBounds.NeighbourhoodHilbertSchmidtHolds
import E1.Formalism.SobolevGaussianKernels.StatementCS
import E1.Formalism.SobolevGaussianKernels.StatementMV
import E1.Formalism.SobolevGaussianKernels.StatementNC

set_option Elab.async false

namespace E1N.M2575
def val : Nat := E1N.M2571.val % 7 + E1N.M2572.val % 7 + E1N.M2573.val % 7 + E1N.M2574.val % 7 + 1
theorem val_pos : 0 < val := by unfold val; omega
theorem w0 (a b : Nat) : a + b + 0 = b + a + 0 := by omega
theorem w1 (a b : Nat) : a + b + 1 = b + a + 1 := by omega
theorem w2 (a b : Nat) : a + b + 2 = b + a + 2 := by omega
theorem w3 (a b : Nat) : a + b + 3 = b + a + 3 := by omega
end E1N.M2575
