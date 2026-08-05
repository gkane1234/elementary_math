# Difficulty → lane selection audit

Overall topic **difficulty D** plus **constraints** choose the number lane; values are then sampled inside that lane at the same effective D.

## Lane unlock thresholds (min D)

| Lane | min D |
|------|------:|
| `friendly_wholes` | 0 |
| `signed_small` | 0 |
| `unit_fractions` | 3 |
| `simple_rations` | 4 |
| `difficult_rations` | 8 |
| `friendly_decimals` | 4 |
| `awkward_decimals` | 10 |

Also open `gallery.html` for a browsable view.

## default

Settings: `{}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes`, `signed_small` | `friendly_wholes`×5, `signed_small`×3 | $1$, $0$, $3$, $1$, $2$, $0$ |
| 2 | `friendly_wholes`, `signed_small` | `signed_small`×6, `friendly_wholes`×2 | $0$, $4$, $4$, $2$, $2$, $4$ |
| 4 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `friendly_decimals` | `unit_fractions`×4, `friendly_decimals`×4 | $\frac{1}{7}$, $\frac{1}{2}$, $0.52$, $-1.1$, $-1$, $\frac{1}{7}$ |
| 6 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `friendly_decimals` | `friendly_decimals`×4, `simple_rations`×2, `unit_fractions`×2 | $-\frac{6}{5}$, $\frac{1}{5}$, $-6.31$, $\frac{1}{8}$, $9.52$, $\frac{1}{2}$ |
| 8 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals` | `difficult_rations`×4, `friendly_decimals`×3, `simple_rations`×1 | $10.67$, $\frac{26}{12}$, $\frac{78}{39}$, $1$, $\frac{45}{42}$, $-10.7$ |
| 10 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×6, `unit_fractions`×1, `difficult_rations`×1 | $\frac{1}{3}$, $-11.344$, $9.314$, $4.59$, $5.146$, $-2.03$ |
| 12 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×5, `difficult_rations`×2, `simple_rations`×1 | $-12.49$, $-\frac{2}{3}$, $12.22$, $\frac{18}{28}$, $-6.252$, $-\frac{12}{36}$ |
| 14 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×5, `difficult_rations`×3 | $-\frac{31}{20}$, $-1.791$, $\frac{12}{10}$, $4.077$, $-15.003$, $\frac{48}{34}$ |

## integers_only (integers_only, no fractions, no decimals)

Settings: `{"integers_only": true}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes`, `signed_small` | `friendly_wholes`×4, `signed_small`×4 | $1$, $1$, $3$, $-3$, $2$, $3$ |
| 2 | `friendly_wholes`, `signed_small` | `signed_small`×4, `friendly_wholes`×4 | $5$, $0$, $1$, $0$, $-5$, $5$ |
| 4 | `friendly_wholes`, `signed_small` | `friendly_wholes`×5, `signed_small`×3 | $-3$, $2$, $7$, $6$, $7$, $-3$ |
| 6 | `friendly_wholes`, `signed_small` | `signed_small`×5, `friendly_wholes`×3 | $-5$, $2$, $7$, $0$, $-1$, $8$ |
| 8 | `friendly_wholes`, `signed_small` | `friendly_wholes`×6, `signed_small`×2 | $4$, $2$, $7$, $11$, $-1$, $4$ |
| 10 | `friendly_wholes`, `signed_small` | `friendly_wholes`×6, `signed_small`×2 | $10$, $0$, $8$, $11$, $7$, $13$ |
| 12 | `friendly_wholes`, `signed_small` | `friendly_wholes`×4, `signed_small`×4 | $2$, $-6$, $12$, $13$, $14$, $1$ |
| 14 | `friendly_wholes`, `signed_small` | `friendly_wholes`×6, `signed_small`×2 | $11$, $14$, $14$, $10$, $16$, $2$ |

## no_decimals (no decimals)

Settings: `{"allow_decimals": false}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes`, `signed_small` | `signed_small`×5, `friendly_wholes`×3 | $2$, $1$, $0$, $1$, $2$, $-3$ |
| 2 | `friendly_wholes`, `signed_small` | `signed_small`×6, `friendly_wholes`×2 | $4$, $-5$, $2$, $0$, $-2$, $0$ |
| 4 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations` | `simple_rations`×7, `unit_fractions`×1 | $1$, $-\frac{1}{5}$, $\frac{5}{2}$, $2$, $1$, $\frac{1}{4}$ |
| 6 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations` | `unit_fractions`×4, `simple_rations`×4 | $\frac{1}{8}$, $\frac{1}{6}$, $\frac{4}{5}$, $\frac{3}{4}$, $-\frac{4}{5}$, $\frac{1}{7}$ |
| 8 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations` | `difficult_rations`×6, `simple_rations`×2 | $\frac{4}{48}$, $-\frac{54}{36}$, $-\frac{14}{12}$, $\frac{63}{15}$, $-\frac{48}{48}$, $\frac{1}{5}$ |
| 10 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations` | `difficult_rations`×7, `unit_fractions`×1 | $-\frac{84}{30}$, $\frac{3}{39}$, $\frac{1}{4}$, $-\frac{34}{8}$, $\frac{29}{11}$, $\frac{112}{24}$ |
| 12 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations` | `difficult_rations`×7, `simple_rations`×1 | $\frac{52}{36}$, $\frac{64}{30}$, $-\frac{18}{14}$, $-\frac{3}{2}$, $-\frac{21}{5}$, $\frac{31}{11}$ |
| 14 | `friendly_wholes`, `signed_small`, `unit_fractions`, `simple_rations`, `difficult_rations` | `difficult_rations`×6, `simple_rations`×2 | $\frac{30}{20}$, $\frac{15}{39}$, $\frac{34}{18}$, $\frac{5}{6}$, $\frac{22}{30}$, $\frac{11}{4}$ |

## no_fractions (no fractions)

Settings: `{"allow_fractions": false}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes`, `signed_small` | `signed_small`×5, `friendly_wholes`×3 | $-2$, $0$, $1$, $-1$, $1$, $-2$ |
| 2 | `friendly_wholes`, `signed_small` | `signed_small`×5, `friendly_wholes`×3 | $-1$, $1$, $1$, $0$, $-2$, $-1$ |
| 4 | `friendly_wholes`, `signed_small`, `friendly_decimals` | `friendly_decimals`×8 | $-2.1$, $-1.5$, $-1.5$, $0.75$, $0.75$, $0.93$ |
| 6 | `friendly_wholes`, `signed_small`, `friendly_decimals` | `friendly_decimals`×8 | $6.96$, $7.71$, $7.55$, $-5$, $9.5$, $5.3$ |
| 8 | `friendly_wholes`, `signed_small`, `friendly_decimals` | `friendly_decimals`×8 | $-3.72$, $3.62$, $-5.69$, $7.1$, $11$, $10.1$ |
| 10 | `friendly_wholes`, `signed_small`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×8 | $-12.24$, $8.09$, $1.319$, $0.66$, $-3.871$, $-12.38$ |
| 12 | `friendly_wholes`, `signed_small`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×8 | $6.961$, $7.591$, $-4.647$, $14.422$, $-7.44$, $-9.19$ |
| 14 | `friendly_wholes`, `signed_small`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×7, `friendly_decimals`×1 | $-4.374$, $8.993$, $4.2$, $2.291$, $10.23$, $-5.67$ |

## positives_only (no negatives)

Settings: `{"allow_negatives": false}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes` | `friendly_wholes`×8 | $0$, $1$, $1$, $3$, $0$, $0$ |
| 2 | `friendly_wholes` | `friendly_wholes`×8 | $4$, $0$, $2$, $1$, $0$, $4$ |
| 4 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `friendly_decimals` | `simple_rations`×3, `unit_fractions`×3, `friendly_decimals`×2 | $\frac{5}{2}$, $\frac{1}{5}$, $\frac{1}{2}$, $4.1$, $\frac{1}{2}$, $\frac{3}{4}$ |
| 6 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `friendly_decimals` | `friendly_decimals`×3, `unit_fractions`×3, `simple_rations`×2 | $5.5$, $1.1$, $\frac{1}{4}$, $\frac{1}{2}$, $\frac{1}{6}$, $\frac{7}{2}$ |
| 8 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals` | `difficult_rations`×5, `friendly_decimals`×3 | $1.28$, $\frac{44}{44}$, $\frac{80}{48}$, $5$, $\frac{16}{8}$, $6.5$ |
| 10 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×6, `friendly_decimals`×1, `difficult_rations`×1 | $7.1$, $8.43$, $11.018$, $12.22$, $7.33$, $\frac{19}{14}$ |
| 12 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `difficult_rations`×5, `awkward_decimals`×3 | $10.82$, $11.61$, $\frac{60}{36}$, $\frac{30}{6}$, $\frac{2}{24}$, $\frac{18}{18}$ |
| 14 | `friendly_wholes`, `unit_fractions`, `simple_rations`, `difficult_rations`, `friendly_decimals`, `awkward_decimals` | `awkward_decimals`×5, `difficult_rations`×3 | $\frac{9}{20}$, $15.51$, $13.437$, $9.252$, $7.52$, $12.477$ |

## integers_no_negatives (integers_only, no negatives, no fractions, no decimals)

Settings: `{"integers_only": true, "allow_negatives": false}`

| D | Eligible lanes | Selected (counts) | Sample values |
|--:|----------------|-------------------|---------------|
| 0 | `friendly_wholes` | `friendly_wholes`×8 | $2$, $2$, $2$, $1$, $3$, $0$ |
| 2 | `friendly_wholes` | `friendly_wholes`×8 | $2$, $3$, $5$, $2$, $4$, $2$ |
| 4 | `friendly_wholes` | `friendly_wholes`×8 | $4$, $1$, $2$, $2$, $3$, $1$ |
| 6 | `friendly_wholes` | `friendly_wholes`×8 | $3$, $3$, $5$, $2$, $6$, $7$ |
| 8 | `friendly_wholes` | `friendly_wholes`×8 | $0$, $1$, $4$, $8$, $7$, $9$ |
| 10 | `friendly_wholes` | `friendly_wholes`×8 | $1$, $6$, $2$, $0$, $4$, $13$ |
| 12 | `friendly_wholes` | `friendly_wholes`×8 | $14$, $10$, $5$, $7$, $10$, $1$ |
| 14 | `friendly_wholes` | `friendly_wholes`×8 | $3$, $17$, $15$, $12$, $1$, $17$ |

