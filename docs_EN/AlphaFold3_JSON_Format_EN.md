<p align="left">
  <a href="./README_EN.md">Homepage</a>
</p>
<p align="right">
  <strong>English</strong> | <a href="../AlphaFold3_JSON_Format.md">中文</a>
</p>

## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### This document shows the common formats for the AF3 input JSON (proteins as the example)
---

> **00 Basic AF3 JSON structure**
```json
{
  "name": "Example",  // job name; the output directory is named after it
  "sequences": [
    {
      "protein": {
        "id": "A",  // chain name; a string "A" for one chain, a list ["A", "B"] for several
        "sequence": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  // amino-acid sequence
      }
    }
  ],
  "modelSeeds": [1],  // list of random seeds; N seeds -> 5N samples, e.g. [1,2] gives 10 outputs
  "dialect": "alphafold3",  // always "alphafold3"
  "version": 1  // always 1
}
```
---

> **01 Single-chain protein**
```json
{
  "name": "LMK1",
  "sequences": [
    {
      "protein": {
        "id": "A",
        "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"
      }
    }
  ],
  "modelSeeds": [1],
  "dialect": "alphafold3",
  "version": 1
}
```

---

> **02 Homomer**
```json
{
  "name": "LMK2",
  "sequences": [
    {
      "protein": {
        "id": ["A", "B"],
        "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"
      }
    }
  ],
  "modelSeeds": [1],
  "dialect": "alphafold3",
  "version": 1
}
```

---

> **03 Heteromer**
```json
{
  "name": "LMK3",
  "sequences": [
    {
      "protein": {
        "id": "A",
        "sequence": "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"
      }
    },
    {
      "protein": {
        "id": "B",
        "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"
      }
    }
  ],
  "modelSeeds": [1],
  "dialect": "alphafold3",
  "version": 1
}
```

---

**The formats below are for the web AlphaFold Server**

---

> **04 Basic structure**
```json
[
  {
    "name": "Example",          // job name; the output directory is named after it
    "modelSeeds": [1],          // at most 1 seed per job; leave [] and the server picks one
    "sequences": [
      {
        "proteinChain": {
          "sequence": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  // amino-acid sequence
          "count": 1            // copies of this chain; 1 for a monomer, 2/3/... for a multimer
        }
      }
    ]
  }
]                               // the whole thing is an array, with no dialect / version
```

---

> **05 Single-chain protein**
```json
[
  {
    "name": "LMK1",
    "modelSeeds": [1],
    "sequences": [
      {
        "proteinChain": {
          "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG",
          "count": 1
        }
      }
    ]
  }
]
```

---

> **06 Homomer**
```json
[
  {
    "name": "LMK2",
    "modelSeeds": [1],
    "sequences": [
      {
        "proteinChain": {
          "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG",
          "count": 2
        }
      }
    ]
  }
]
```

---

> **07 Heteromer**
```json
[
  {
    "name": "LMK3",
    "modelSeeds": [1],
    "sequences": [
      {
        "proteinChain": {
          "sequence": "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL",
          "count": 1
        }
      },
      {
        "proteinChain": {
          "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG",
          "count": 1
        }
      }
    ]
  }
]
```

---

> **08 Field mapping: local open-source AF3 ↔ web AlphaFold Server**

| Aspect                | Local open-source AF3 (00-03)        | Web AlphaFold Server (04-07)                             |
| --------------------- | ------------------------------------ | -------------------------------------------------------- |
| Top level             | a single object `{ }`                | an array `[ { }, … ]` (several jobs at once)             |
| Protein               | `"protein"` + `"id"`                 | `"proteinChain"` + `"count"`                             |
| Multimer              | id list `["A", "B"]`                 | `"count": 2`                                             |
| Chain id              | assigned by hand                     | assigned by the server                                   |
| DNA / RNA             | `"dna"` / `"rna"` + `id`             | `"dnaSequence"` / `"rnaSequence"` + `count`              |
| Ligand                | `"ligand"` + `ccdCodes` / `smiles`   | `"ligand": "CCD_XXX"` + `count` (allow-listed CCDs only) |
| Ion                   | folded into the ligand ccdCode       | its own `"ion"` field                                    |
| `dialect` / `version` | required                             | none                                                     |
| `modelSeeds`          | required; `[1,2,…]` may hold several | at most **1** per job (leave `[]` for random)            |

---


##### [AlphaFold3 official documentation](https://github.com/google-deepmind/alphafold3)
##### [AlphaFold Server help](https://alphafoldserver.com/faq)
