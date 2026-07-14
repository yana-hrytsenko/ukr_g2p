# =============================================================================
# rules.py  —  rule types + indexed engine
# =============================================================================
 
from dataclasses import dataclass, field
from .symbols import *
from .utils import prev_token, next_token
from .phonemas import *





@dataclass
class CombinatoryModificationRule:

    name:        str
    
    type:        str  
    patterns:    list
    direction:   str = None

    stop:        set = field(default_factory=lambda: HARD_STOP)
    skip:        set = field(default_factory=lambda: {' '})


@dataclass
class AssimilationPattern:

    trigger:     object
    target:      object

    map:         object  

@dataclass
class AccommodationPattern:

    trigger:     object
    target:      object


@dataclass
class PositionalModificationRule:

    name:        str
    condition:   object    

    patterns:    list           

    stop:        set = field(default_factory=lambda: HARD_STOP)
    skip:        set = field(default_factory=lambda: {' '})

@dataclass
class PositionalPattern:

    phoneme:     set
    context:     object
    allophone:   str


@dataclass
class QuantitativeModificationRule:

    name:       str

    trigger:    callable  


# =============================================================================
# engines
# =============================================================================

def apply_assimilation_pattern(token, pattern):
    if pattern.target(token):
        if token.char in pattern.map:
            token.char = pattern.map[token.char]
            token.features = set(PHONES.get(token.char, []))
            if "soft" in token.features:
                token.palatalization = True

def apply_accommodation_pattern(token, rule, pattern):
    if pattern.target(token):
        if rule.name not in token.modifications:
            token.modifications.add(rule.name)
            if rule.name == "semipalatalization":
                token.palatalization = True

def apply_propagation(tokens, i, rule, pattern):
    directions = []
    if rule.direction in ('regressive', 'bidirectional'):
        directions.append(-1)
    if rule.direction in ('progressive', 'bidirectional'):
        directions.append(1)
    for step in directions:
        j = i
        while True:
            if step == -1:
                token, j = prev_token(tokens, j, stop=rule.stop, skip=rule.skip)
            else:
                token, j = next_token(tokens, j, stop=rule.stop, skip=rule.skip)
            if token is None:
                break
            if isinstance(pattern, AssimilationPattern):
                apply_assimilation_pattern(token, pattern)
                break
            elif isinstance(pattern, AccommodationPattern):
                apply_accommodation_pattern(token, rule, pattern)
                break
 
def apply_combinatory_rule(tokens, rule):
    for i, token in enumerate(tokens):
        for pattern in rule.patterns:
            if pattern.trigger(token):
                apply_propagation(tokens, i, rule, pattern)
    return tokens
 
 
def apply_positional_rule(tokens, rule):
    for i, token in enumerate(tokens):
        prv, _ = prev_token(tokens, i, stop=rule.stop, skip=rule.skip)
        nxt, _ = next_token(tokens, i, stop=rule.stop, skip=rule.skip)
        token.index = i
        token.tokens = tokens
        if rule.condition and not rule.condition(token, prv, nxt):
            continue
        for pattern in rule.patterns:
            if token.char not in pattern.phoneme:
                continue
            if pattern.context is None or pattern.context(token, prv, nxt):  
                '''If allophone is a function, run it and store its result.'''
                if callable(pattern.allophone):
                    token.allophone = pattern.allophone(token)
                else:
                    token.allophone = pattern.allophone
                break
    return tokens

    
def apply_quantitative_rule(tokens, rule):
    i = 0
    while i < len(tokens) - 1:
        a = tokens[i]
        b = tokens[i + 1]
        if rule.trigger(a, b):
            a.long_start = True
            b.long_end = True
        i += 1
    return tokens
 
# =============================================================================
# dispatcher
# =============================================================================
 
def apply_modifications(tokens, rules):
    for rule in rules:
        if isinstance(rule, CombinatoryModificationRule):
            tokens = apply_combinatory_rule(tokens, rule)
        elif isinstance(rule, PositionalModificationRule):
            tokens = apply_positional_rule(tokens, rule)
        elif isinstance(rule, QuantitativeModificationRule):
            tokens = apply_quantitative_rule(tokens, rule)    
    return tokens




