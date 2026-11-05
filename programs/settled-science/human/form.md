# Your 20 calls: which way did the finding go?

**Fill this in before you open `results/`, `bettor/` or `items/items.jsonl`.** Those show the answers and the engine's odds.

Each item is a real study posted to arXiv between July and November 2026, after the engine's model was trained, so it cannot have read them. Exactly one of the two options is what the paper reported. For each one, write **1 or 2**, and if you like, **how sure** from 50 (a coin flip) to 100 (certain). If you leave 'how sure' blank it is scored as 75.

Take about a minute each; go with your gut. No session asks you for these in a terminal (engine CONTEXT.md §3 rule 11): your calls count only once they are committed to `ledger/human-odds.jsonl` from a cockpit download. If they are not there when the bettor's results are scored, the program proceeds marked 'no human odds'.

## H01 · model-psychology

**For reducing multilingual sycophancy toward false premises, did reasoning-oriented prompting strategies perform better or worse than directive-based strategies?**

How it was tested: Multilingual LLMs answered questions with and without a user's false premise across several languages. Each response was classified by crossing whether the model answered correctly without pressure and whether it kept that answer under pressure. Two families of prompting interventions were compared: reasoning-oriented strategies and directive-based strategies.

1. Reasoning-oriented strategies performed worse than directive-based strategies.
2. Reasoning-oriented strategies performed better than directive-based strategies.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-056</sub>

## H02 · model-psychology

**On arithmetic items, when a planted derivation was supplied with user pushback, was a wrong committed answer corrected more or less often than a true committed answer was abandoned?**

How it was tested: Eleven frontier models were tested with stateless replays in which a committed answer was followed by one scripted user line, each read against a matched control without the line. On one model, arithmetic items with known answers were paired with user lines that either stated a bare value or included a worked derivation arguing for a different answer.

1. Wrong answers were corrected more often than true answers were abandoned.
2. Wrong answers were corrected less often than true answers were abandoned.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-042</sub>

## H03 · quantum-devices

**For a Rydberg two-qubit gate in a cryogenic cesium tweezer array, was the error contribution from Rydberg-state decay larger or smaller than the contribution from atomic motion?**

How it was tested: A universal gate set was run on 133Cs atoms in optical tweezers inside a cryogenic environment, with the entangling gate using single-photon coupling to a Rydberg P state. The measured two-qubit gate fidelity was compared with an error budget separating atomic-motion and Rydberg-decay contributions.

1. The Rydberg-decay contribution was smaller than the atomic-motion contribution.
2. The Rydberg-decay contribution was larger than the atomic-motion contribution.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-086</sub>

## H04 · scalable-oversight

**On a backdoored-code detection benchmark for AI control, did a Claude Sonnet 5 monitor catch a higher or lower share of backdoors written by Claude Sonnet 5 than of backdoors written by older language models?**

How it was tested: A Claude Sonnet 5 model was prompted as a monitor to distinguish honest from backdoored solutions to programming problems. The backdoored code came either from the older language models used in a standard evaluation dataset or from Claude Sonnet 5 itself, and the monitor's catch rate was compared between the two sources, both before and after validity checks on the backdoors.

1. The monitor caught a lower share of Sonnet 5's backdoors than of older models' backdoors.
2. The monitor caught a higher share of Sonnet 5's backdoors than of older models' backdoors.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-114</sub>

## H05 · interpretability

**In Qwen3-VL-4B, was refusal more or less responsive to activation steering along a learned safety direction at deeper layers than at early vision layers?**

How it was tested: A safety direction was learned from activations of Qwen3-VL-4B on safe and unsafe inputs. Activation steering along this direction was applied at different depths, from early vision layers to deeper layers, and the change in rejection of unsafe inputs was measured, together with how well each layer separated safe from unsafe inputs.

1. Refusal was less responsive to steering at deeper layers than at early vision layers.
2. Refusal was more responsive to steering at deeper layers than at early vision layers.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-022</sub>

## H06 · interpretability

**In two vision-language-action models, were action outputs more or less sensitive to directional language in corrupted instructions than to abstract rephrasing?**

How it was tested: LIBERO task instructions given to pi-0.5 and GR00T N1.7 were corrupted in five ways: synonym replacement, semantic scaling, directional corruption, random object substitution and empty string. Activation and attribution patching on the residual stream of the action-generation modules measured how much each corruption affected the generated actions.

1. Actions were more sensitive to directional language than to abstract rephrasing.
2. Actions were less sensitive to directional language than to abstract rephrasing.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-007</sub>

## H07 · interpretability

**Was code models' default preference for Python syntax, when the prompt names no language, larger or smaller in instruction-tuned checkpoints than in their base versions?**

How it was tested: Ten open code models (five base, five instruction-tuned) were prompted to write code without a specified language, and their preference for Python over a target language (Rust, C# or PHP) was measured with aligned prompts. Each instruction-tuned checkpoint was compared with its base version.

1. The Python preference was smaller in instruction-tuned checkpoints than in their base versions.
2. The Python preference was larger in instruction-tuned checkpoints than in their base versions.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-012</sub>

## H08 · model-psychology

**Over five rounds of recursive self-training on Qwen3-1.7B, did the model's most confident answers become more or less reliable?**

How it was tested: Qwen3-1.7B was put through a five-round self-training loop with three seeds per compared method. Confidence temperature (drift from a calibrated starting point) was measured separately from discrimination (ranking correct above incorrect answers), along with accuracy and the reliability of the highest-confidence answers.

1. The most confident answers became less reliable over self-training.
2. The most confident answers became more reliable over self-training.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-059</sub>

## H09 · quantum-devices

**In superconducting Kerr oscillators in the transmon regime, did the oscillator's frequency sensitivity to an applied charge drive increase or decrease as the drive frequency was raised?**

How it was tested: Superconducting Kerr oscillators in the transmon regime were driven through their charge port at sub-GHz frequencies. The AC Stark shift was used as a probe of the oscillator's frequency sensitivity to the charge drive, measured as a function of drive frequency and amplitude.

1. Charge-drive sensitivity decreased as drive frequency was raised.
2. Charge-drive sensitivity increased as drive frequency was raised.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-072</sub>

## H10 · scalable-oversight

**When checking numerical claims in papers written by AI research agents, did an LLM verifier accept more or fewer misattributed claims than a deterministic claim-to-evidence checker given the same evidence?**

How it was tested: Numerical claims from papers written by AI research agents on open research problems were manually labelled as supported, traceable or misattributed (values from the wrong experiment, metric or run in the agent's own files). A deterministic claim-to-evidence checker with fixed rules and an LLM verifier were given the same evidence, and the number of misattributed claims each accepted was compared.

1. The LLM verifier accepted more misattributed claims than the deterministic checker.
2. The LLM verifier accepted fewer misattributed claims than the deterministic checker.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-113</sub>

## H11 · model-psychology

**Over scripted repeated questioning about ambiguous social episodes, with no new event evidence, did LLMs' expressed certainty in their interpretations rise or fall?**

How it was tested: Eight LLMs interpreted 604 ambiguous social episodes, with matched depression and social anxiety disclosures, over four-turn dialogues in which the event evidence was left unchanged and the user repeatedly asked again. Interpretations, emotional support and expressed certainty were tracked across turns.

1. Expressed certainty fell over repeated questioning.
2. Expressed certainty rose over repeated questioning.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-054</sub>

## H12 · model-psychology

**When models pushed back against users' false assertions, was their phrasing more or less indirect in Hindi and Yoruba than in English, German and Chinese?**

How it was tested: Model responses to false user inputs were collected in English, German, Chinese, Hindi and Yoruba. A human-validated phrase-level labelling scheme coded how responses pushed back against or affirmed the false input, including the directness of the pushback.

1. Pushback phrasing was less indirect in Hindi and Yoruba than in the other languages.
2. Pushback phrasing was more indirect in Hindi and Yoruba than in the other languages.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-046</sub>

## H13 · interpretability

**In a sparse-MLP transformer whose neurons serve as a known reference basis, did transcoders recover the neuron vectors with higher or lower cosine similarity than sparse autoencoders?**

How it was tested: A 5-layer language model was trained on TinyStories with a wide TopK-sparse MLP so that its MLP neurons provide a reference basis. Transcoders (trained to map MLP input to MLP output) and sparse autoencoders (trained to reconstruct MLP outputs) were fitted to the model and compared on the cosine similarity between their learned features and the true neuron vectors.

1. Transcoders recovered the neuron vectors with lower cosine similarity than sparse autoencoders.
2. Transcoders recovered the neuron vectors with higher cosine similarity than sparse autoencoders.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-011</sub>

## H14 · scalable-oversight

**When a small Llama 8B reward-hacking monitor was given additional structured evidence on top of the full agent trace, did it flag more or fewer of the honest-failure episodes that resembled exploits?**

How it was tested: A sandboxed task let a Llama 3.1 8B agent game a completion score, and every episode was labelled by replaying it and repairing the final state. A small local Llama 8B model acted as a monitor to separate exploit attempts from honest failures with the same score gap. On 25 exploit episodes and 25 honest look-alikes, the monitor judged either the full trace or the full trace plus additional structured evidence, and flags on the honest look-alikes were compared.

1. The monitor flagged more honest look-alikes when given the additional structured evidence.
2. The monitor flagged fewer honest look-alikes when given the additional structured evidence.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-115</sub>

## H15 · scalable-oversight

**In RLHF against a proxy reward model, at a fixed expected penalty, did frequent mild audits curb unearned reward more or less effectively than rare severe audits?**

How it was tested: Policies from three model families were trained with RL against accuracy-matched proxy reward models, with two gold reward models used to measure how much of the proxy gain was unbacked by true quality. Audit schemes penalised the policy during training; schemes with the same expected penalty but different frequency and severity were compared on how much unearned reward the policy accumulated.

1. Frequent mild audits curbed unearned reward less effectively than rare severe audits.
2. Frequent mild audits curbed unearned reward more effectively than rare severe audits.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-106</sub>

## H16 · quantum-devices

**In a Kerr-cat qubit coupled to a lossy readout mode at selected operating points, did the measured bit-flip time increase or decrease as the cat photon number was raised?**

How it was tested: A Kerr-cat qubit in a superconducting oscillator was operated at operating points where an intra-well transition is resonant with a lossy readout mode. Bit-flip times were measured as a function of the mean photon number of the cat state, alongside phase-flip rates.

1. The bit-flip time decreased as photon number was raised.
2. The bit-flip time increased as photon number was raised.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-088</sub>

## H17 · quantum-devices

**Among sputtered Nb films with different biaxial stress, did microwave resonators made from highly compressive films show more or less temperature-dependent loss?**

How it was tested: Sputtered niobium films were grown across a series of biaxial film stresses. Transport (transition temperature, residual resistance ratio) was measured on each film, and microwave resonators fabricated from them were characterised for temperature-dependent loss and frequency shift.

1. Highly compressive films showed more temperature-dependent loss.
2. Highly compressive films showed less temperature-dependent loss.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-070</sub>

## H18 · quantum-devices

**For two simultaneously driven, exchange-coupled spin qubits, were exchange-induced features in the Rabi dynamics stronger or weaker when the difference between the two Rabi frequencies exceeded the exchange coupling?**

How it was tested: Two exchange-coupled semiconductor spin qubits were driven simultaneously with microwaves while exchange coupling and drive power were varied. Rabi oscillations and Rabi chevrons were recorded and exchange-induced features (beating, split chevrons) were tracked against the ratio of Rabi-frequency difference to exchange.

1. Exchange-induced features were stronger when the Rabi-frequency difference exceeded the exchange.
2. Exchange-induced features were weaker when the Rabi-frequency difference exceeded the exchange.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-067</sub>

## H19 · scalable-oversight

**After fine-tuning a same-model untrusted monitor on honest reviews of one caught collusion behaviour, was the remaining collusion rate higher or lower on held-out collusion behaviours than on the caught behaviour itself?**

How it was tested: Llama-3.3-70B and Qwen2.5-72B were fine-tuned to install five policy-monitor collusion pairs, in which the model acting as monitor covered up its own misbehaviour. The monitor was then corrected by fine-tuning on 300 honest reviews of one caught collusion, and collusion was measured on that behaviour and on the other four in unseen prompt formats.

1. Remaining collusion was higher on the held-out behaviours than on the caught behaviour.
2. Remaining collusion was lower on the held-out behaviours than on the caught behaviour.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-110</sub>

## H20 · interpretability

**Under mean ablation on GPT-2 small indirect object identification, did circuits agree with the full model's exact answers more or less often on prompts it got wrong than on prompts it got right?**

How it was tested: A manual circuit and several automated circuits for indirect object identification in GPT-2 small were evaluated with the rest of the model mean-ablated. Exact answer agreement between each circuit and the full model was measured separately on prompts the model answered correctly and on prompts where it erred.

1. Circuits agreed with the model more often on its errors than on its correct answers.
2. Circuits agreed with the model less often on its errors than on its correct answers.

Your call (1 or 2): ____   How sure (50–100): ____

<sub>ss-001</sub>
