## Lamarck &nbsp; &nbsp; &nbsp; 2026-04-29
#### 该文档用于展示 AF3 输入 JSON 的常见格式（以蛋白质为例）
---

> **00 AF3 JSON 基本结构**
```json
{
  "name": "Example",  // 任务名，输出目录会以此命名
  "sequences": [
    {
      "protein": {
        "id": "A",  // 链的名称，单链写字符串 "A"，多链写列表 ["A", "B"]
        "sequence": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  // 氨基酸序列
      }
    }
  ],
  "modelSeeds": [1],  // 随机种子列表，长度 N → 输出 5N 个 sample → 例如 [1,2] 对应 10 个输出
  "dialect": "alphafold3",  // 固定写 "alphafold3"
  "version": 1  // 固定写 1
}
```
---

> **01 单链蛋白**
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

> **02 同源多聚体**
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

> **03 异源多聚体**
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

**以下为网页版 AlphaFold Server 的写法**

---

> **04 基本结构**
```json
[
  {
    "name": "Example",          // 任务名，输出目录以此命名
    "modelSeeds": [1],          // 每个 job 上限 1 个 seed；留空 [] 则服务器随机
    "sequences": [
      {
        "proteinChain": {
          "sequence": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  // 氨基酸序列
          "count": 1            // 该链拷贝数，单体写 1，多聚体写 2/3/...
        }
      }
    ]
  }
]                               // 整体是数组，且无 dialect / version
```

---

> **05 单链蛋白**
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

> **06 同源多聚体**
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

> **07 异源多聚体**
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

> **08 本地开源版 ↔ 网页版 (AlphaFold Server) 字段对照**

| 维度                  | 本地开源 AF3（00–03）              | 网页 AlphaFold Server（04–07）                  |
| --------------------- | ---------------------------------- | ----------------------------------------------- |
| 顶层                  | 单个对象 `{ }`                     | 数组 `[ { }, … ]`（一次可放多个任务）           |
| 蛋白                  | `"protein"` + `"id"`               | `"proteinChain"` + `"count"`                    |
| 多聚体                | id 列表 `["A", "B"]`               | `"count": 2`                                    |
| 链 id                 | 手动指定                           | 服务器自动分配                                  |
| DNA / RNA             | `"dna"` / `"rna"` + `id`           | `"dnaSequence"` / `"rnaSequence"` + `count`     |
| 配体                  | `"ligand"` + `ccdCodes` / `smiles` | `"ligand": "CCD_XXX"` + `count`（仅白名单 CCD） |
| 离子                  | 归入 ligand 的 ccdCode             | 独立 `"ion"` 字段                               |
| `dialect` / `version` | 必需                               | 无                                              |
| `modelSeeds`          | 必填，`[1,2,…]` 可多个             | 每个 job 上限 **1 个**（留空 `[]` 则随机）      |

---


##### [AlphaFold3官方文档](https://github.com/google-deepmind/alphafold3)
##### [AlphaFold Server 帮助文档](https://alphafoldserver.com/faq)
