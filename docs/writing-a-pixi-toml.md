# Writing a `pixi.toml` from scratch

A `pixi.toml` is the environment spec file for [Pixi](https://pixi.sh) — it plays the
same role as `environment.yml` for conda or `requirements.txt` for pip, but it
can pull packages from **both** conda-forge and PyPI in a single, reproducible
solve. This guide walks through building one by hand once you already know
which packages you need.

---

## 1. The minimal skeleton

Every `pixi.toml` needs a `[workspace]` table and at least one dependency:

```toml
[workspace]
name = "my-project"
version = "0.1.0"
channels = ["conda-forge"]
platforms = ["osx-arm64", "linux-64"]

[dependencies]
python = "3.11.*"
```

- `name` / `version` — free text, just metadata.
- `channels` — where conda packages come from. `conda-forge` covers the vast
  majority of scientific Python packages; only add more (e.g. `bioconda`) if a
  specific package needs it.
- `platforms` — which machines this environment must solve for. Common values:
  `"osx-arm64"` (Apple Silicon Mac), `"osx-64"` (Intel Mac), `"linux-64"`,
  `"win-64"`. Pixi solves dependencies **separately for each platform you
  list**, so only list the ones you actually use — every extra platform is
  more solve time and more chances a package isn't available there.

You don't have to write this by hand: `pixi init` in an empty directory
generates this skeleton for you.

---

## 2. Adding your known packages

Let's say you already know which packages you want. Two ways to add them:

### Option A — let pixi do it (recommended)

```bash
pixi add numpy pandas scikit-learn      # conda-forge packages
pixi add --pypi some-pip-only-package   # PyPI-only packages
```

This edits `pixi.toml` for you and immediately tries to solve/lock the
environment, so you find out right away if something doesn't resolve.

### Option B — edit the TOML directly

```toml
[dependencies]
python = "3.11.*"
numpy = ">=1.24"
pandas = "*"
scikit-learn = ">=1.3"

[pypi-dependencies]
some-pip-only-package = "*"
```

- `[dependencies]` → conda-forge packages. **Prefer this table** for anything
  with compiled/binary components (numpy, scipy, pandas, scikit-learn,
  pyarrow, geopandas, torch, etc.) — conda-forge ships prebuilt binaries and
  its solver accounts for them, whereas pip has to build or download
  large wheels and can "backtrack" for a long time trying to satisfy
  constraints.
- `[pypi-dependencies]` → packages that either don't exist on conda-forge, or
  that you need at a specific git ref / local path (see §5).

**How do I know if a package is on conda-forge?** Search
[prefix.dev](https://prefix.dev) or run `pixi search <package-name>`. If it's
not there, it goes in `[pypi-dependencies]` instead.

---

## 3. Version constraints

You don't need every package pinned — `"*"` means "any version, let the
solver pick." Use constraints when a package requires it:

| Syntax | Meaning |
|---|---|
| `"*"` | any version |
| `">=1.24"` | at least 1.24 |
| `"1.11.*"` | any 1.11.x patch release |
| `">=1.17.1,<2"` | range (inclusive lower, exclusive upper) |

A good rule of thumb: leave things unconstrained (`"*"` or a loose `>=`)
unless you've hit a real incompatibility, a released bug, or a library that
explicitly requires a minimum version for a feature you use. Over-pinning
makes it *harder* to combine your file with others later (see §6).


## 4. Installing a package from git or a local path

If one of your "known packages" isn't published to PyPI/conda-forge — e.g.
it's your own in-development code — `[pypi-dependencies]` supports both:

```toml
[pypi-dependencies]
# from a GitHub repo
my-package = { git = "https://github.com/user/my-package.git" }

# from a local folder, editable (local edits reflected without reinstalling)
my-package = { path = "../my-package", editable = true }
```

Use `git =` when you just need to consume the package as-is. Use
`path = ..., editable = true` when you're actively developing that package
alongside your project.

---

## 6. If you need more than one environment in the same file

Sometimes you have two sets of packages that don't solve together (e.g. two
different pinned versions of the same underlying binary dependency). Instead
of two separate `pixi.toml` files, you can define named **features** and
compose them into separate **environments** in one file:

```toml
[environments]
envA = { features = ["a"], no-default-feature = true }
envB = { features = ["b"], no-default-feature = true }

[feature.a.dependencies]
numpy = "*"

[feature.b.dependencies]
numpy = ">=2,<3"
```

Each environment is solved independently, so `envA` and `envB` can have
conflicting constraints without breaking each other. Run with
`pixi run -e envA <command>`. This repo's own `pixi.toml` is a real example —
see the `toast` and `dotpy` features/environments in it.

---

## 7. Validate it

After writing (or editing) `pixi.toml`, always check it actually solves
before committing:

```bash
pixi lock          # solves and writes pixi.lock — errors here mean a real conflict
pixi install       # installs into .pixi/envs/
pixi run python -c "import numpy; print(numpy.__version__)"   # smoke test
```

If `pixi lock` fails, read the error message closely — it usually names the
exact two constraints that can't both be satisfied, which tells you which
version range to loosen.
