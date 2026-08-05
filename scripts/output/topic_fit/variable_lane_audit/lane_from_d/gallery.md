# Difficulty → variable lane selection audit

Overall topic **difficulty D** plus **constraints** choose the variable lane; letters are then sampled inside that lane.

## Lane unlock thresholds (min D)

| Lane | min D | Pool sketch |
|------|------:|-------------|
| `only_x` | 0 | Always the letter x. |
| `xyz` | 3 | Classic Cartesian / multi-variable intro letters. |
| `abctuvwxyz` | 6 | School set: a–c, h, k, m–n, p–z (no d–g, i–j, l, o). |
| `whole_alphabet` | 10 | Any lowercase Latin letter a–z. |
| `greek` | 12 | Common Greek variables (α β γ δ θ λ μ … ω); not π/ε/ι. |

Also open `gallery.html` for a browsable view.

## default

Settings: `{}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x`, `xyz` | `xyz`×8 | $x$, $x$, $x$, $z$, $y$, $z$, $y$, $x$ |
| 6 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×8 | $b$, $u$, $r$, $n$, $c$, $z$, $p$, $v$ |
| 8 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×6, `xyz`×2 | $p$, $s$, $r$, $z$, $y$, $q$, $x$, $a$ |
| 10 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet` | `whole_alphabet`×6, `abctuvwxyz`×2 | $u$, $x$, $m$, $a$, $w$, $e$, $i$, $b$ |
| 12 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet`, `greek` | `greek`×5, `whole_alphabet`×3 | $f$, $\beta$, $\rho$, $f$, $\mu$, $n$, $\rho$, $\tau$ |
| 14 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet`, `greek` | `whole_alphabet`×5, `abctuvwxyz`×2, `greek`×1 | $q$, $o$, $q$, $\xi$, $c$, $e$, $n$, $k$ |

## only_x (only_x)

Settings: `{"only_x": true}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 6 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 8 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 10 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 12 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 14 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |

## no_greek (no greek)

Settings: `{"allow_greek": false}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x`, `xyz` | `xyz`×8 | $z$, $y$, $x$, $x$, $z$, $x$, $z$, $y$ |
| 6 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×6, `xyz`×2 | $t$, $h$, $r$, $s$, $t$, $x$, $y$, $m$ |
| 8 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×6, `only_x`×1, `xyz`×1 | $x$, $z$, $y$, $t$, $k$, $q$, $r$, $k$ |
| 10 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet` | `whole_alphabet`×6, `only_x`×1, `abctuvwxyz`×1 | $v$, $z$, $q$, $h$, $w$, $x$, $w$, $o$ |
| 12 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet` | `whole_alphabet`×7, `abctuvwxyz`×1 | $v$, $h$, $a$, $l$, $x$, $b$, $e$, $k$ |
| 14 | `only_x`, `xyz`, `abctuvwxyz`, `whole_alphabet` | `whole_alphabet`×5, `abctuvwxyz`×3 | $y$, $c$, $u$, $f$, $i$, $x$, $a$, $p$ |

## max_xyz (max=xyz)

Settings: `{"max_variable_lane": "xyz"}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x`, `xyz` | `xyz`×7, `only_x`×1 | $z$, $x$, $z$, $x$, $x$, $x$, $z$, $z$ |
| 6 | `only_x`, `xyz` | `xyz`×8 | $y$, $y$, $z$, $z$, $z$, $z$, $z$, $z$ |
| 8 | `only_x`, `xyz` | `xyz`×8 | $x$, $z$, $z$, $z$, $y$, $z$, $y$, $x$ |
| 10 | `only_x`, `xyz` | `xyz`×8 | $z$, $x$, $y$, $x$, $y$, $z$, $y$, $z$ |
| 12 | `only_x`, `xyz` | `xyz`×8 | $z$, $y$, $z$, $y$, $x$, $y$, $z$, $x$ |
| 14 | `only_x`, `xyz` | `xyz`×8 | $y$, $y$, $z$, $z$, $z$, $x$, $y$, $z$ |

## max_common (max=abctuvwxyz)

Settings: `{"max_variable_lane": "abctuvwxyz"}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x`, `xyz` | `xyz`×7, `only_x`×1 | $x$, $x$, $y$, $x$, $y$, $x$, $y$, $z$ |
| 6 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×7, `xyz`×1 | $k$, $p$, $h$, $n$, $h$, $m$, $a$, $x$ |
| 8 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×8 | $w$, $m$, $s$, $c$, $m$, $a$, $h$, $u$ |
| 10 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×6, `xyz`×2 | $b$, $h$, $v$, $s$, $y$, $y$, $a$, $n$ |
| 12 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×7, `xyz`×1 | $r$, $z$, $p$, $r$, $b$, $x$, $w$, $k$ |
| 14 | `only_x`, `xyz`, `abctuvwxyz` | `abctuvwxyz`×7, `xyz`×1 | $u$, $s$, $c$, $t$, $z$, $t$, $b$, $v$ |

## legacy_no_other_letters (only_x)

Settings: `{"allow_other_letters": false}`

| D | Eligible lanes | Selected (counts) | Sample letters |
|--:|----------------|-------------------|----------------|
| 0 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 2 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 4 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 6 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 8 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 10 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 12 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |
| 14 | `only_x` | `only_x`×8 | $x$, $x$, $x$, $x$, $x$, $x$, $x$, $x$ |

