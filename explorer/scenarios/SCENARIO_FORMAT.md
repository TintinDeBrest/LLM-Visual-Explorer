# LlmExpl Scenario YAML Format

**Version:** 1.0

A scenario defines the set of concepts explored by LlmExpl, together with
optional human annotations and visual references.

The format deliberately separates:

- the concept represented by the language model;
- human semantic annotations;
- display information;
- visual resources and their provenance.

---

# Fundamental rule

> **Only the `concept` field is used as input to the language model.**

All other fields are metadata used by LlmExpl.

Fields such as `short_name`, `category`, `emoji`, `image`, `search_query`,
language information, identifiers and image credits must not modify the
semantic representation computed from `concept`.

---

# 1. Scenario structure

A scenario has the following general structure:

```yaml
family: animals
language: en

title: Animals
description: Exploration of animal concepts.

concepts:

  - concept: Dog
    emoji: 🐕
    category: mammals

  - concept: Eagle
    emoji: 🦅
    category: birds
```

## Scenario-level fields

| Field | Status | Description |
|---|---|---|
| `family` | Recommended | Identifier shared by related scenarios, especially language variants |
| `language` | Recommended | Default language of the scenario |
| `title` | Required | Human-readable scenario title |
| `description` | Required | Short explanation of the purpose of the scenario |
| `concepts` | Required | List of concepts explored in the scenario |

---

## `family`

Identifies a family of related scenarios.

Example:

```yaml
family: animals
```

The same family may have several language versions:

```text
animals_en.yaml
animals_fr.yaml
animals_es.yaml
```

---

## `language`

Default language of the concepts in the scenario.

Example:

```yaml
language: fr
```

A concept may optionally specify its own `language`, particularly in
multilingual scenarios.

---

## `title`

Human-readable title displayed by LlmExpl.

```yaml
title: Iconic Cars
```

---

## `description`

Short pedagogical description of the scenario.

```yaml
description: Exploration of the semantic space of twelve iconic French and international cars.
```

---

## `concepts`

List of concepts studied by LlmExpl.

Each entry is a YAML mapping containing at least a `concept` field.

```yaml
concepts:

  - concept: Dog

  - concept: Wolf
```

---

# 2. Concept fields

## Core fields

| Field | Status | Description |
|---|---|---|
| `concept` | **Required** | Text represented by the language model |
| `id` | Recommended | Stable technical identifier for this scenario entry |
| `short_name` | Optional | Short display label |
| `language` | Optional | Language of this particular concept |
| `concept_id` | Optional | Human identifier grouping semantically equivalent entries |
| `category` | Optional | Human semantic category |

## Presentation fields

| Field | Status | Description |
|---|---|---|
| `emoji` | Optional | Visual marker used in the interface |
| `image` | Optional | Local visual reference |
| `search_query` | Optional | Suggested web search when a visual is not distributed |

## Image provenance fields

| Field | Status | Description |
|---|---|---|
| `image_credit` | Optional | Author / creator attribution |
| `image_license` | Optional | Human-readable license |
| `image_license_url` | Optional | Reference page for the license |
| `image_source` | Optional | Original source of the image |

---

# 3. The concept represented by the model

## `concept`

`concept` is the central field of every entry.

```yaml
- concept: Peugeot 404
```

or:

```yaml
- concept: Mettre la main à la pâte
```

It contains the text used to compute the semantic representation.

Changing `concept` may therefore change the experiment.

A display requirement must never cause `concept` to be shortened, translated
or rewritten.

Only this field is used as input to the language model.

---

# 4. Technical identity and display

## `id`

`id` identifies a particular entry in the scenario.

```yaml
- id: peugeot_404
  concept: Peugeot 404
```

It is intended to remain stable independently of presentation changes.

`id` is never sent to the language model.

---

## `short_name`

Optional shorter label used when the complete concept would make a
visualization difficult to read.

```yaml
- concept: Mettre la main à la pâte
  short_name: Main à la pâte
```

Typical uses include:

- 2D maps;
- 3D planetariums;
- dendrograms;
- compact labels.

When `short_name` is absent, LlmExpl should display `concept`.

Conceptually:

```python
display_name = item.get("short_name", item["concept"])
```

`short_name` must never replace `concept` when computing the model
representation.

---

# 5. Human semantic annotations

## `category`

Optional human classification of a concept.

```yaml
- concept: Dog
  category: animals
```

Categories may be used to compare human semantic classifications with
structures observed in the model, for example clusters or dendrograms.

A category represents **human reference information**.

It must never be used to influence the embedding or other model
representation being studied.

---

## `concept_id`

`concept_id` groups several entries that humans intend to represent the same
underlying concept.

This is especially useful for multilingual experiments.

```yaml
- id: house_fr
  concept_id: house
  language: fr
  concept: Maison

- id: house_en
  concept_id: house
  language: en
  concept: House

- id: house_es
  concept_id: house
  language: es
  concept: Casa
```

Here, the experiment can ask whether the model places `Maison`, `House`
and `Casa` close together.

`concept_id` expresses the human experimental reference.

It is not supplied to the model.

---

# 6. Language

For ordinary monolingual scenarios, language should normally be specified
once at scenario level:

```yaml
language: fr
```

A concept-level language may be used when necessary:

```yaml
- concept: House
  language: en
```

This is particularly useful in multilingual scenarios.

Concept-level `language` takes precedence over the scenario default for
metadata and display purposes.

Language metadata must not be added to the text represented by the model
unless an experiment explicitly defines such behavior.

---

# 7. Visual references

Visual references exist for the human user and are independent of the
language-model representation.

## Local image

```yaml
- id: peugeot_404
  concept: Peugeot 404
  image: cars/peugeot_404.jpg
  image_credit: Jeremy
  image_license: CC BY 2.0
  image_license_url: https://creativecommons.org/licenses/by/2.0/
  image_source: https://commons.wikimedia.org/wiki/File:...
```

LlmExpl may display the image together with its attribution.

The image is **not sent to the language model**.

---

## `search_query`

Some visual references cannot or should not be distributed with LlmExpl,
notably for copyright reasons.

In this case, the scenario may provide a search query instead:

```yaml
- concept: Guernica
  search_query: Picasso Guernica painting
```

LlmExpl can offer the user a way to search for the visual reference without
including or distributing the protected image.

`search_query` is an editorial instruction for visual discovery, not semantic
input to the model.

---

# 8. Minimal scenario

The smallest canonical Version 1 scenario is:

```yaml
title: Simple example
description: Minimal LlmExpl scenario.

concepts:

  - concept: Dog

  - concept: Wolf
```

For normal published scenarios, `family` and `language` are strongly
recommended:

```yaml
family: animals
language: en

title: Animals
description: Exploration of animal concepts.

concepts:

  - concept: Dog

  - concept: Wolf
```

---

# 9. Rich concept example

A concept may combine several optional annotations:

```yaml
- id: peugeot_404
  concept: Peugeot 404
  short_name: 404
  category: french_car
  emoji: 🇫🇷

  image: cars/peugeot_404.jpg
  image_credit: Jeremy
  image_license: CC BY 2.0
  image_license_url: https://creativecommons.org/licenses/by/2.0/
  image_source: https://commons.wikimedia.org/wiki/File:...
```

All fields except `concept` are metadata.

---

# 10. Visual reference without a distributed image

When an image cannot or should not be included in LlmExpl:

```yaml
- id: guernica
  concept: Guernica
  emoji: 🖼️
  search_query: Picasso Guernica painting
```

No image is distributed by LlmExpl.

The search query merely helps the user find a visual reference independently.

---

# 11. Multilingual example

A multilingual scenario may explicitly associate different linguistic forms
with the same human concept:

```yaml
family: multilingual
title: Multilingual concepts
description: Comparison of equivalent concepts across languages.

concepts:

  - id: house_fr
    concept_id: house
    language: fr
    concept: Maison
    emoji: 🏠

  - id: house_en
    concept_id: house
    language: en
    concept: House
    emoji: 🏠

  - id: house_es
    concept_id: house
    language: es
    concept: Casa
    emoji: 🏠
```

The three values of `concept` are independently represented by the model.

`concept_id: house` records the human experimental hypothesis that they refer
to the same underlying concept.

LlmExpl may then investigate whether their model representations are
actually close.

---

# 12. Version 1 canonical rules

1. The top-level collection is named `concepts`.
2. Every entry in `concepts` is a YAML mapping.
3. Every entry has a `concept` field.
4. `concept` contains the text represented by the language model.
5. Only `concept` is used as model input.
6. `short_name` affects display only.
7. `category` contains human classification information only.
8. `concept_id` may associate several entries with the same human concept.
9. Visual fields affect the human interface only.
10. Image attribution must be preserved when a distributed image requires it.
11. `search_query` may be used when a visual reference is not distributed.
12. Scenario and concept language fields are metadata and are not
    automatically added to model input.
13. Metadata must never silently modify the semantic representation being
    studied.

---
# 13 Filename convention

Monolingual scenario filenames follow the canonical convention:

```text
<scenario_identifier>_<language>.yaml
```

Examples:

```text
animals_en.yaml
animals_fr.yaml
animals_es.yaml

cars_en.yaml
cars_fr.yaml

Grim_3x6_en.yaml
Grim_3x6_fr.yaml
Grim_3x6_es.yaml
```

The language code is always the final component before `.yaml`.

Standard language codes currently used by LlmExpl include:

```text
en    English
fr    French
es    Spanish
```

The scenario identifier may include a family name and an optional variant:

```text
<family>_<variant>_<language>.yaml
```

Examples:

```text
animals_genetics_en.yaml
Grim_3x6_en.yaml
```

For monolingual scenarios, the filename language suffix and the scenario
`language` field should agree.

## Multilingual scenarios

A scenario that is intrinsically multilingual does not use a language suffix.

Example:

```text
multilingual.yaml
```

In such a scenario, individual concepts may specify their language:

```yaml
concepts:

  - id: house_fr
    concept_id: house
    language: fr
    concept: Maison

  - id: house_en
    concept_id: house
    language: en
    concept: House

  - id: house_es
    concept_id: house
    language: es
    concept: Casa
```

The filename convention is intended for file organization and scenario
discovery.

The metadata stored inside the YAML remains authoritative.

---

# 14. Legacy formats

Earlier LlmExpl scenarios may use:

```yaml
objects:

  - name: Dog

  - name: Wolf
```

or a simple list:

```yaml
concepts:

  - Dog

  - Wolf
```

These are legacy representations.

The canonical Version 1 representation is:

```yaml
concepts:

  - concept: Dog

  - concept: Wolf
```

Migration from a legacy scenario must preserve the original semantic input:

```text
legacy name  →  concept
```

No concept should be renamed, translated, shortened or otherwise altered
during format migration.

---

# 15. Design principle

The scenario format separates two viewpoints:

```text
HUMAN / EXPERIMENT                         LANGUAGE MODEL

scenario
│
├── category
├── concept_id
├── language
├── short_name
├── emoji
├── image
├── visual provenance
│
└── concept  ─────────────────────────────► model input
```

This separation is fundamental to LlmExpl.

Human annotations describe the experiment and help interpret its results.

They must not be confused with information available to the language model.