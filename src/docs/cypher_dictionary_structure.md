# Cypher dictionary nodes with properties

```json

NeoDictionary {created_at: STRING, authors_ref: STRING, disable_metadata: BOOLEAN, ntealan: BOOLEAN, disable: BOOLEAN, abbr_name: STRING, last_update: STRING, search_vector: STRING, review_year: INTEGER, publication: STRING, locked: BOOLEAN, uid: STRING, ref_parent: STRING, short_name: STRING, long_name: STRING, description: STRING, id_dico: STRING, source: STRING, in_editing: BOOLEAN, visibility: STRING, viewers: INTEGER, review_version: STRING, verified: BOOLEAN}
NeoArticle {created_at: STRING, type_article: STRING, ntealan: BOOLEAN, disable: BOOLEAN, id: INTEGER, html_version: STRING, xml_version: STRING, last_update: STRING, uid: STRING, name: STRING, locked: BOOLEAN, id_dico: STRING, ref_parent: STRING, raw_data: STRING, visibility: STRING, viewers: INTEGER, verified: BOOLEAN, in_editing: BOOLEAN}
NeoTag {description: STRING, uid: STRING, name: STRING, created_at: STRING, disable: BOOLEAN, last_update: STRING, ntealan: BOOLEAN}
NeoWord {NeoLanguage {status: STRING, spoken_countries: LIST, classification: STRING, iso_code: STRING, spoken_area: STRING, dialects: LIST, spoken_region: STRING, uid: STRING, name: STRING, ntealan: BOOLEAN, alternate_names: STRING}
created_at: STRING, id: INTEGER, disable: BOOLEAN, locked: BOOLEAN, value: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoRadical {type: STRING, created_at: STRING, disable: BOOLEAN, locked: BOOLEAN, value: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoVariant {created_at: STRING, disable: BOOLEAN, locked: BOOLEAN, type: STRING, id: INTEGER, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoEntry {disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoCategory {created_at: STRING, id: INTEGER, ref_parent: STRING, disable: BOOLEAN, locked: BOOLEAN, abbr_name: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, long_name: STRING, in_editing: BOOLEAN, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoCategories {disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoTranslation {created_at: STRING, content: STRING, number: STRING, ref_parent: STRING, disable: BOOLEAN, locked: BOOLEAN, language: STRING, uid: STRING, context: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoTranslations {disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoExample {target: STRING, created_at: STRING, origin: STRING, ref_parent: STRING, disable: BOOLEAN, locked: BOOLEAN, number: STRING, uid: STRING, ref_node: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoExamples {disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoNominalPair {type: STRING, disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoSingularClass {created_at: STRING, type: STRING, disable: BOOLEAN, locked: BOOLEAN, value: INTEGER, id: INTEGER, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoPluralClass {created_at: STRING, type: STRING, disable: BOOLEAN, locked: BOOLEAN, value: INTEGER, id: INTEGER, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoClasses {type: STRING, disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoPrefix {type: STRING, created_at: STRING, disable: BOOLEAN, locked: BOOLEAN, value: STRING, id: INTEGER, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoVariantConjugation {locked: BOOLEAN, created_at: STRING, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, disable: BOOLEAN, uid: STRING, form_conj: STRING, viewers: INTEGER, verified: BOOLEAN, visibility: STRING, last_update: STRING, type_conj: STRING}
NeoConjugations {created_at: STRING, ref_parent: STRING, disable: BOOLEAN, locked: BOOLEAN, uid: STRING, verified: BOOLEAN, name: STRING, ntealan: BOOLEAN, in_editing: BOOLEAN, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoSuffix {type: STRING, created_at: STRING, ref_parent: STRING, disable: BOOLEAN, locked: BOOLEAN, value: STRING, uid: STRING, verified: BOOLEAN, name: STRING, ntealan: BOOLEAN, in_editing: BOOLEAN, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoGroupNominalPair {type: STRING, disable: BOOLEAN, locked: BOOLEAN, created_at: STRING, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
NeoNeutralClass {type: STRING, created_at: STRING, disable: BOOLEAN, locked: BOOLEAN, value: INTEGER, id: INTEGER, uid: STRING, verified: BOOLEAN, ntealan: BOOLEAN, in_editing: BOOLEAN, ref_parent: STRING, visibility: STRING, last_update: STRING, viewers: INTEGER}
```

# Cypher relations between nodes


```json

(:NeoDictionary)-[:RESOURCE_HAVE_TAG]->(:NeoTag)
(:NeoDictionary)-[:RESOURCE_IS_CREATED_BY]->(:NeoUser)
(:NeoDictionary)-[:RESOURCE_HAVE_COMMENT]->(:NeoComment)
(:NeoDictionary)-[:DICTIONARY_IS_USED_IN]->(:NeoCommunity)
(:NeoDictionary)-[:SUBMITTED_IN]->(:NeoLicense)
(:NeoArticle)-[:ARTICLE_IS_USED_IN]->(:NeoDictionary)
(:NeoArticle)-[:ARTICLE_USE_ENTRY]->(:NeoEntry)
(:NeoArticle)-[:ARTICLE_USE_CATEGORIES]->(:NeoCategories)
(:NeoArticle)-[:ARTICLE_USE_TRANSLATIONS]->(:NeoTranslations)
(:NeoArticle)-[:ARTICLE_USE_EXAMPLES]->(:NeoExamples)
(:NeoArticle)-[:RESOURCE_IS_CREATED_BY]->(:NeoUser)
(:NeoArticle)-[:SUBMITTED_IN]->(:NeoLicense)
(:NeoArticle)-[:ARTICLE_USE_CLASSES]->(:NeoClasses)
(:NeoArticle)-[:ARTICLE_USE_CONJUGATION]->(:NeoConjugations)
(:NeoArticle)-[:USER_CONTRIBUTE_WITH]->(:NeoContribution)
(:NeoArticle)-[:RESOURCE_HAVE_COMMENT]->(:NeoComment)
(:NeoLanguage)-[:EXAMPLE_USE_LANGUAGE]->(:NeoExample)
(:NeoWord)-[:WORD_IS_USED_IN]->(:NeoVariant)
(:NeoRadical)-[:RADICAL_IS_FOUND_IN]->(:NeoWord)
(:NeoEntry)-[:ENTRY_USE_DV]->(:NeoVariant)
(:NeoCategory)-[:GC_IS_USED_IN]->(:NeoCategories)
(:NeoTranslation)-[:WT_IS_USED_IN]->(:NeoTranslations)
(:NeoExample)-[:CONTEXTUALISATION]->(:NeoExamples)
(:NeoNominalPair)-[:NP_IS_USED_IN]->(:NeoClasses)
(:NeoSingularClass)-[:SG_CLASS_IS_USED_IN]->(:NeoNominalPair)
(:NeoSingularClass)-[:SG_CLASS_IS_USED_IN]->(:NeoGroupNominalPair)
(:NeoPluralClass)-[:PL_CLASS_IS_USED_IN]->(:NeoNominalPair)
(:NeoPluralClass)-[:PL_CLASS_IS_USED_IN]->(:NeoGroupNominalPair)
(:NeoPrefix)-[:CP_IS_FOUND_IN]->(:NeoWord)
(:NeoVariantConjugation)-[:VC_IS_USED_IN]->(:NeoConjugations)
(:NeoSuffix)-[:CS_IS_FOUND_IN]->(:NeoWord)
(:NeoGroupNominalPair)-[:GROUP_NP_IS_USED_IN]->(:NeoClasses)
(:NeoNeutralClass)-[:UNKNOWN_CLASS_IS_USED_IN]->(:NeoNominalPair)
```