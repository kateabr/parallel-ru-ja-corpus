(: Corpus-specific database functions :)
xquery version "3.1" encoding "utf-8";

module namespace corpus = "http://parallel-ru-ja-corpus.com";

declare function corpus:load-entry($dbName as xs:string, $entryId as xs:string) {
    for $entry in collection($dbName)/entry
    where $entry/id = $entryId
    return $entry
};

declare function corpus:load-sentence($dbName as xs:string, $entryId as xs:string, $sentenceId as xs:integer) {
    for $entry in collection($dbName)/entry
    for $sentence in $entry/sentencePairs/sentencePair
    where $entry/id = $entryId and $sentence/id = $sentenceId
    return $sentence
};

(: Full-Text Search :)
declare function corpus:full-text-result($entry as element(), $sentencePair as element()) as element() {
    element result {
       element entryId { $entry/id/string() },
       element entryTitle { $entry/title/russian, $entry/title/japanese },
       element entryUrl { $entry/url/russian, $entry/url/japanese },
       $sentencePair
    }
};

declare function corpus:full-text-search-japanese-regex($dbName as xs:string, $query as xs:string) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $sentence in $pair/japanese/sentence
    where matches($sentence, $query)
    return corpus:full-text-result($entry, $pair)
};
declare function corpus:full-text-search-japanese($dbName as xs:string, $query as xs:string) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $sentence in $pair/japanese/sentence
    where contains($sentence, $query)
    return corpus:full-text-result($entry, $pair)
};
declare function corpus:full-text-search-russian-regex($dbName as xs:string, $query as xs:string) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $sentence in $pair/russian/sentence
    where matches($sentence, $query)
    return corpus:full-text-result($entry, $pair)
};
declare function corpus:full-text-search-russian($dbName as xs:string, $query as xs:string) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $sentence in $pair/russian/sentence
    where contains($sentence, $query)
    return corpus:full-text-result($entry, $pair)
};
declare function corpus:full-text-search(
    $dbName as xs:string,
    $language as xs:string,
    $query as xs:string,
    $regex as xs:boolean,
    $offset as xs:double,
    $limit as xs:double
) {
    let $startTime := prof:current-ms()
    let $matches :=
        if ($language = "RUSSIAN") then
            if ($regex) then
                corpus:full-text-search-russian-regex($dbName, $query)
            else
                corpus:full-text-search-russian($dbName, $query)
        else if ($language = "JAPANESE") then
            if ($regex) then
                corpus:full-text-search-japanese-regex($dbName, $query)
            else
                corpus:full-text-search-japanese($dbName, $query)
        else ()
    let $results := element results { if ($limit <= 0) then $matches else subsequence($matches, $offset, $limit) }
    let $endTime := prof:current-ms()

    return element searchResult {
        element totalCount { count($matches) },
        element request {
            element database { $dbName },
            element language { $language },
            element query { $query },
            element regex { $regex },
            element offset { $offset - 1 },
            element limit { $limit },
            element elapsedTime { $endTime - $startTime }
        },
        $results
    }
};

(: Token-Based Search :)
declare function corpus:token-text-result($entry, $sentencePair, $tokenId) {
    element result {
        element entryId { $entry/id/string() },
        element entryTitle { $entry/title/russian, $entry/title/japanese },
        element entryUrl { $entry/url/russian, $entry/url/japanese },
        element tokenIds { $tokenId },
        (: $pair will return a sequence, documentation:
            ... and every variable that appears in the pre-grouping tuples
            that were assigned to that group is represented by a variable of the same name,
            bound to a sequence of all values bound to the variable in any of these pre-grouping tuples.
        :)
        $sentencePair[1]
    }
};

declare function corpus:token-has-all-attributes(
    $tokenAttributes as element(),
    $queryAttributes as map(xs:string, xs:string)
) {
    let $mapTokenAttributes := map:merge(
         for $attr in $tokenAttributes/attribute
         let $name := $attr/name/string()
         let $value := $attr/value/string()
         return map { $name : $value }
     )

    return fn:fold-left(
    map:keys($queryAttributes),
    true(),
    function($acc, $key) {
        if ($acc = false()) then false()
        else (
            let $queryElem := map:get($queryAttributes, $key)
            let $attrElem := map:get($mapTokenAttributes, $key)
            return $acc and exists($queryElem) and $queryElem = $attrElem
        )
    })
};
declare function corpus:token-has-all-extra-attributes(
    $tokenAttributes as element(),
    $queryAttributes as xs:string*
) as xs:boolean {
    let $seqTokenAttributes := for $token in $tokenAttributes return $token/extraAttribute/string()
    return fn:fold-left(
        $queryAttributes,
        true(),
        function($acc as xs:boolean, $elem as xs:string) as xs:boolean {
            if ($acc = false()) then false()
            else (
                let $idx := index-of($seqTokenAttributes, $elem)
                return $acc and exists($idx)
            )
    })
};

declare function corpus:token-search-word-russian(
    $dbName as xs:string,
    $query as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*
) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $tokens in $pair/russian/tokens
    for $token in $tokens/token
    where $query = $token/text
        and corpus:token-has-all-attributes($token/attributes, $attributes)
        and corpus:token-has-all-extra-attributes($token/extraAttributes, $extraAttributes)
    group by $entryId := $entry/id, $pairId := $pair/id
    return corpus:token-text-result($entry,$pair, $token/id)
};
declare function corpus:token-search-lexeme-russian(
    $dbName as xs:string,
    $query as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*
) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $tokens in $pair/russian/tokens
    for $token in $tokens/token
    where $query = $token/lexeme
        and corpus:token-has-all-attributes($token/attributes, $attributes)
        and corpus:token-has-all-extra-attributes($token/extraAttributes, $extraAttributes)
    group by $entryId := $entry/id, $pairId := $pair/id
    return corpus:token-text-result($entry,$pair, $token/id)
};

declare function corpus:token-search-word-japanese(
    $dbName as xs:string,
    $query as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*
) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $tokens in $pair/japanese/tokens
    for $token in $tokens/token
    where $query = $token/text
        and corpus:token-has-all-attributes($token/attributes, $attributes)
        and corpus:token-has-all-extra-attributes($token/extraAttributes, $extraAttributes)
    group by $entryId := $entry/id, $pairId := $pair/id
    return corpus:token-text-result($entry,$pair, $token/id)
};
declare function corpus:token-search-lexeme-japanese(
    $dbName as xs:string,
    $query as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*
) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $tokens in $pair/japanese/tokens
    for $token in $tokens/token
    where $query = $token/lexeme
        and corpus:token-has-all-attributes($token/attributes, $attributes)
        and corpus:token-has-all-extra-attributes($token/extraAttributes, $extraAttributes)
    group by $entryId := $entry/id, $pairId := $pair/id
    return corpus:token-text-result($entry,$pair, $token/id)
};
declare function corpus:token-search-normal-form-japanese(
    $dbName as xs:string,
    $query as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*
) {
    for $entry in collection($dbName)/entry
    for $pair in $entry/sentencePairs/sentencePair
    for $tokens in $pair/japanese/tokens
    for $token in $tokens/token
    where $query = $token/normalForm
        and corpus:token-has-all-attributes($token/attributes, $attributes)
        and corpus:token-has-all-extra-attributes($token/extraAttributes, $extraAttributes)
    group by $entryId := $entry/id, $pairId := $pair/id
    return corpus:token-text-result($entry,$pair, $token/id)
};

declare function corpus:token-search(
    $dbName as xs:string,
    $language as xs:string,
    $query as xs:string,
    $mode as xs:string,
    $attributes as map(xs:string, xs:string),
    $extraAttributes as xs:string*,
    $offset as xs:double,
    $limit as xs:double
) {
    let $startTime := prof:current-ms()

    let $matches :=
        if ($language = "RUSSIAN") then
            if ($mode = "WORD") then
                corpus:token-search-word-russian($dbName, $query, $attributes, $extraAttributes)
            else if ($mode = "LEXEME") then
                corpus:token-search-lexeme-russian($dbName, $query, $attributes, $extraAttributes)
            else ()
        else if ($language = "JAPANESE") then
            if ($mode = "WORD") then
                corpus:token-search-word-japanese($dbName, $query, $attributes, $extraAttributes)
            else if ($mode = "LEXEME") then
                corpus:token-search-lexeme-japanese($dbName, $query, $attributes, $extraAttributes)
            else if ($mode = "NORMAL_FORM") then
                corpus:token-search-normal-form-japanese($dbName, $query, $attributes, $extraAttributes)
            else ()
        else ()
    let $results := element results { if ($limit <= 0) then $matches else subsequence($matches, $offset, $limit) }
    let $endTime := prof:current-ms()

    return element searchResult {
        element totalCount { count($matches) },
        element request {
            element database { $dbName },
            element language { $language },
            element query { $query },
            element searchMode { $mode },
            element attributes { map:for-each($attributes,
                function ($k, $v) {
                        element attribute {
                            element name { $k },
                            element value { $v }
                        }
                    })
            },
            element extraAttributes { for $ea in $extraAttributes return element extraAttribute { $ea } },
            element offset { $offset - 1 },
            element limit { $limit },
            element elapsedTime { $endTime - $startTime }
        },
        $results
    }
};
