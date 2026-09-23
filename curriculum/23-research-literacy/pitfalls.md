# Module 23 pitfalls

## Citing a paper's abstract as if it verifies its technical details

An abstract confirms a paper exists and states its framing -- it rarely
contains enough detail to verify a specific formula, hyperparameter, or
methodology choice. This module's own worked example (lesson 03) needed a
*second*, independent source (Hugging Face TRL's current docs) to actually
confirm GRPO's exact advantage formula, because the abstract alone didn't
contain it. Don't let confirming a paper's existence and general claims
substitute for verifying the specific detail you actually need.

## Treating a failed PDF text extraction as "unverifiable" instead of trying a different source

This module's own research process hit a real, mundane obstacle: an
attempt to read the DeepSeekMath paper's raw PDF returned mostly binary/
image data instead of usable text. The fix wasn't to give up on
verification -- it was to find a different, independent, current source
(Hugging Face's TRL documentation) that stated the same technical claim in
an actually extractable form. A source being hard to read isn't the same
as a claim being unverifiable; try another angle before marking something
UNVERIFIED.

## Over-crediting a paper's reported numbers because "it's peer-reviewed" or "it's from a well-known lab"

Neither peer review nor institutional reputation substitutes for the
specific checks lesson 01 describes (baseline quality, eval-set
independence, variance reporting) -- both are weak, indirect signals about
average quality across many papers, not a guarantee about the specific
claim you're currently trying to evaluate.

## Conflating "I understand the paper's idea" with "I have verified the paper's claim"

Understanding *what* GRPO's formula is (this curriculum's Module 21 lab
implements it correctly) is a different accomplishment than verifying
*that the paper's own reported results* actually hold under scrutiny
(baseline comparisons, eval methodology, reproducibility). This module's
own worked example is explicit about only having done the former for
DeepSeekMath's benchmark claims -- don't let building a correct
implementation of an idea stand in for having actually audited the paper's
evidence for its broader claims.
