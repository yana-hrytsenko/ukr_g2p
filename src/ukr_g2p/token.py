from dataclasses import dataclass, field


@dataclass
class Token:
    
    char:           str
    allophone:      str  | None = None

    stress:         bool = False
    palatalization: bool = False

    long_start:     bool = False
    long_end:       bool = False

    features:       set =  field(default_factory=set)
    modifications:  set =  field(default_factory=set)

    
    def token_is(self, feature: str) -> bool:
        return feature in self.features
    
    def _is_not(self, feature: str) -> bool:
        return feature not in self.features
    
    def _is_both(self, *features: str) -> bool:
        return all(f in self.features for f in features)

    def _is_either(self, *features: str) -> bool:
        return any(f in self.features for f in features)

    def has(self, attr: str) -> bool:
        return bool(getattr(self, attr, None))

    def has_no(self, attr: str) -> bool:
        return not bool(getattr(self, attr, None))
    
    def has_mod(self, modification: str) -> bool:
        return modification in self.modifications
    

    
def phoneme_is(*features):
    return lambda t: all(f in t.features for f in features)

def phoneme_is_either(*features): 
    return lambda t: any(f in t.features for f in features)

def phoneme_is_not(*features):
    return lambda t: all(f not in t.features for f in features) 

def phoneme_has(*attrs):
    return lambda t: all(getattr(t, a, False) for a in attrs)

def phoneme_has_either(*attrs): 
    return lambda t: any( getattr(t, a, False) for a in attrs)

def phoneme_has_no(*attrs):
    return lambda t: all(not getattr(t, a, False) for a in attrs)

def either(*predicates):
    return lambda t: any(p(t) for p in predicates)

def both(*predicates):
    return lambda t: all(p(t) for p in predicates)





    