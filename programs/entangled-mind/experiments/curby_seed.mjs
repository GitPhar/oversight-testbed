// Beacon seed for a bet (oversight-testbed/operators/hardware.md), using @buff-beacon-project/curby-client@1.2.0.
//
//   CURBY_CLIENT=<path to node_modules/@buff-beacon-project/curby-client> node experiments/curby_seed.mjs check
//       -> CURBY-Q's latest completed round and its time (recorded in the pre-registration before committing)
//   CURBY_CLIENT=... node experiments/curby_seed.mjs rng <commit-iso-time>
//       -> the first CURBy-RNG pulse timestamped after the commit, the pulse before it, and the randomness hex
//
// The seed itself is then derived with oversight-testbed/ledger/seed.py <randomness-hex> <bet-id> --purpose <p>.
import { pathToFileURL } from 'node:url'
import path from 'node:path'

const lib = await import(pathToFileURL(path.join(process.env.CURBY_CLIENT, 'dist', 'index.js')).href)
const { Client, DIRNGClient } = lib
setTimeout(() => { console.error('timeout'); process.exit(2) }, 120000)
const hex = b => Buffer.from(b).toString('hex')
const [mode, when] = process.argv.slice(2)

if (mode === 'check') {
  const d = await DIRNGClient.create().latest()
  const t = d.pulses.result?.value?.content?.payload?.timestamp
  console.log(JSON.stringify({ chain: 'CURBY-Q', latest_completed_round: d.round, stage: d.stage, result_pulse_time_utc: t,
    checked_at_utc: new Date().toISOString(), client: '@buff-beacon-project/curby-client@1.2.0' }, null, 1))
} else if (mode === 'rng') {
  const commit = new Date(when)
  const c = Client.create()
  const time = async i => new Date((await c.fetchPulsePair(i)).pulse.value.content.payload.timestamp)
  const latest = (await c.fetchPulsePair()).pulse
  let i = latest.value.content.index
  if (new Date(latest.value.content.payload.timestamp) <= commit) { console.error('no pulse after the commit yet'); process.exit(3) }
  // walk back (pulses are one minute apart) to the last pulse at or before the commit
  while (await time(i - 1) > commit) i -= 1
  const pair = await c.fetchPulsePair(i)
  const rand = await c.randomness(i)
  console.log(JSON.stringify({ chain: 'CURBy-RNG', pulse_index: i, pulse_time_utc: pair.pulse.value.content.payload.timestamp,
    previous_index: i - 1, previous_time_utc: (await time(i - 1)).toISOString(), commit_time_utc: commit.toISOString(),
    randomness: hex(rand.bytes()), client: '@buff-beacon-project/curby-client@1.2.0', certificate_verified: false }, null, 1))
} else {
  console.error('usage: check | rng <commit-iso-time>'); process.exit(1)
}
process.exit(0)
