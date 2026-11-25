import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.DegSupermod
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.DegSupermodZ
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.DiscreteSpanOfLinIndep
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.DualPl
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.Duality
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.Example
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.ExistsSmulMemOfFinrankEq
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.FinSup
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.FrameHermSharpB
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.FrameLinearAlgebraFirst
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.GramBlock
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.HNExtreme
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.HNSlopes
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.HNStep
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.HtGram
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.HtImage
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.MuChar
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.PiSumForallInsertOnly
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.PlaceSplit
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.PolygonSlopeSum
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.QuotRealize
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.RatioMax
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.Rerealize
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.RescaleCovol
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.SatBasic
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.ShiftInvariance
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.SizeIneq
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.SizeMu
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.SlopeIneq
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.SlopeIneqMean
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.TheoremFSharp
import E1.Formalism.HarderNarasimhan.HarderNarasimhanProofs.TwistFinrankEq

set_option Elab.async false

namespace E1N.M443
def val : Nat := E1N.M410.val % 7 + E1N.M411.val % 7 + E1N.M412.val % 7 + E1N.M413.val % 7 + 1
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
theorem w12 (a b : Nat) : a + b + 12 = b + a + 12 := by omega
end E1N.M443
