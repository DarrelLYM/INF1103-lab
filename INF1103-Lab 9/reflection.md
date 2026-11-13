# INF1103 Lab 9 – Reflection

My Predict First answers and the Section 1.5 diagnose notes are in *Lab 9 Predict First Notes.docx*.

## What changed from Lab 8

| Change | Where | Why |
|---|---|---|
| Strategy pattern | `discount_strategy.py`: abstract `DiscountStrategy` with `apply(total)`, plus `NoDiscount`, `PercentageDiscount`, `BulkDiscount` and `StudentDiscount` | Each discount is its own class. `Order` is given a strategy (default `NoDiscount()`), can swap it with `set_discount()`, and `calculate_total()` only calls `self.__discount.apply(total)`. There is no discount if/elif in `Order`. |
| Factory pattern | `product_factory.py`: `ProductFactory.create(product_type, ...) -> Product` | The menu, `FileHandler` and the CSV loader all ask the factory for products. Only the factory calls the `PhysicalProduct` and `DigitalProduct` constructors. An unknown type raises `ValueError("Unknown product type: ...")`. |
| Validation | `Product` (price > 0, stock >= 0), `OrderLine` (quantity > 0), discount constructors | Each rule sits in the class that owns the data, so every caller gets the same check. |
| User input | `input_helpers.py`: `get_positive_float()`, `get_non_negative_int()`, `get_positive_int()` | They keep asking until the value is valid, so the menu never carries on with half-entered data. |
| Loading from CSV | `product_loader.py`: `load_products()` and `products.csv`, menu option 10 | Uses try / except / else / finally. A missing file is reported, and each row has its own try / except ValueError so one bad row is skipped and the rest still load. |
| Other error handling | `load_inventory()` and `save_inventory()` in `inventory_manager.py` | A damaged `inventory.json` (`json.JSONDecodeError`) now starts with the default data instead of crashing, and a failed save (`OSError`) is reported. |

The UML (`uml_class_diagram.svg` / `.png`) adds `DiscountStrategy` and its four subclasses, the `Order 0..* —— 1 DiscountStrategy` association, and `ProductFactory` with a dashed «creates» dependency to `Product`. Validation rules are shown as constraints, e.g. `-price: float {> 0}`.

## Testing

- `python lab9_demo.py` runs through Sections 2–5 and prints what I used to check my predictions.
- `python -m unittest discover -s tests -v` runs 56 tests (the 21 Lab 8 tests plus 35 new ones in `test_discounts.py`, `test_product_factory.py`, `test_validation.py` and `test_error_handling.py`). These need no input and no network, so they could run in a CI pipeline on every push.

Every `except` names a specific exception (`ValueError`, `FileNotFoundError`, `KeyError`, `json.JSONDecodeError`, `OSError`). `test_no_bare_or_broad_except` checks there is no bare `except:` or `except Exception`.

## Reflection (Section 8)

**Where would a pattern make things more complicated than needed?** The main menu. It is a long if/elif on the option number, but each option just calls one function, and the options don't change at runtime. Turning every option into a Command class would add a lot of classes for no real benefit. The same goes for `Supplier`: there is only one kind, so a factory for it would just wrap the constructor.

**The Factory moved the OCP issue into the factory. Is that a good trade-off?** Yes for this system. Before, three places had their own if/else for product types. Now there is one. Adding a type still means editing `ProductFactory.create()`, but it's one small method and all the type rules are in one place. A registry would remove the if/elif, but with only two product types it would be more code to read than it saves.

**When would rejecting the whole CSV be better than skipping bad rows?** When the rows depend on each other or a partial load would be misleading. For example, a stock-take file meant to replace the whole inventory, or a price update where half the products getting new prices and half keeping old ones would be worse than no change. Then I would check every row first and only add products if all of them are valid.

**Validation failure vs exception.** A validation failure is my own rule being broken, checked with an `if`, e.g. `if quantity <= 0: raise ValueError("Quantity must be greater than zero.")` in `OrderLine`. An exception is something Python raises when an operation can't be done, e.g. `float("abc")` raising `ValueError` or `open()` raising `FileNotFoundError` in `load_products()`. My validation also raises `ValueError`, so a caller can handle both with one `except ValueError`, like `get_positive_float()` and the CSV loader do.

**Which predictions didn't match?** Three were close but not exact. In 5.1 I expected `12.50` back but `float()` gives `12.5`. The two decimals only appear when formatting. In 5.2 I thought the "abc" price would be rejected by my price > 0 check, but `float("abc")` failed first inside `Product.__init__`, so the message came from Python. In 3.3 I forgot that the menu also lists the product types, so it needs one new entry for a new type even though it doesn't create products itself.

**Strategy or Factory in our group project?** Our incident triage system already has both ideas:

- `exporters/` uses a factory. `ExporterFactory.create(name)` returns an `IncidentExporter`, either CSV or JSON, so the export code only works with the base type. This is the same trade-off as `ProductFactory`: a new format means one new class and one change in the factory.
- The AI enrichment steps in `ai_manager.py` are close to Strategy. `EnrichmentStep` is an abstract class with `run()`, and `HazardFlagStep` and `ReviewStep` each implement it. Every step is called through the same `safe_run()` without the caller knowing which one it is, so the weather and web search steps we are adding are new classes, not new branches.
- A factory for AI clients would be over-engineering right now. We only use one Gemini client and it is passed into the steps when they are created. If we later switched between several providers at runtime, a client factory would start to make sense.
