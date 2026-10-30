# INF1103 Lab 7 – Notes & Reflection

## Design summary

| Concept | Where it is used |
|---|---|
| **Inheritance** (is-a) | `PhysicalProduct(Product)` – a guitar *is-a* physical product; `DigitalProduct(Product)` – an operating system *is-a* digital product. Both reuse `Product.__init__` through `super().__init__(...)`. |
| **Method overriding** | `display_information()` and `to_dict()` are overridden in both subclasses. Each one calls `super()` first so the parent handles the common fields (ID, name, price, stock) and the child only adds its own field (weight / download size). |
| **Abstract class** | `Product` inherits from `ABC` and declares `@abstractmethod get_fulfilment_info()`. Trying `Product("P1", "x", 1, 1)` raises `TypeError: Can't instantiate abstract class Product without an implementation for abstract method 'get_fulfilment_info'`. |
| **Interface (ABC)** | `CanBeShipped` declares only `@abstractmethod calculate_shipping_cost()` with no attributes. `PhysicalProduct` implements it (rule: $5.00 base + $2.00 per kg). `DigitalProduct` does not, because digital products are never shipped. |
| **Single class inheritance** | `PhysicalProduct` has one parent *class* (`Product`) plus one *interface* (`CanBeShipped`). |
| **SRP** | `Product` and its subclasses manage one product each, `Inventory` manages the collection, `FileHandler` handles JSON persistence, and `inventory_manager` handles user input and output. |
| **OCP** | `Product` was not changed to add the new product types. They were added by *extending* it. The only change to `Product` was adding `ABC`, the abstract method and `to_dict()`, all of which are its own responsibility. |

**JSON persistence:** each product builds its own dictionary through `to_dict()`, and the subclass adds `"type": "physical"` or `"type": "digital"` plus its extra field. When loading, `FileHandler` reads `"type"` and creates the matching subclass.

**Testing:** `test_lab7.py` has 17 unit tests that cover every item in Section 7. Run them with `python -m unittest -v test_lab7`.

## Section 8 – Optional reflection: adding a `SubscriptionProduct`

**How well does the current design support a new product type?**
Partly. A `SubscriptionProduct(Product)` class with a `duration_months` attribute can be written without touching `Product`, `Inventory`, `PhysicalProduct` or `DigitalProduct`. That part follows the Open/Closed Principle: `Inventory` only calls methods defined on `Product` (`get_product_id()`, `display_information()`), so it works with any new subclass automatically. The same is true of `FileHandler.save()`, because each product builds its own dictionary with `to_dict()`.

**Which parts needed to change?**
1. `FileHandler.__create_product()` needs a new `if product_type == "subscription"` branch.
2. `inventory_manager.add_product()` needs a new menu option and a new input prompt (`duration_months`).

Both of these are *modified* each time a new type is added, so they are not closed for modification.

**How could the design remove those changes?**
Not with more inheritance, but with a **registry / factory** (composition):
- Keep a dictionary that maps a type identifier to the class, for example `PRODUCT_TYPES = {"physical": PhysicalProduct, "digital": DigitalProduct}`.
- Give each subclass a `from_dict(data)` class method, and a description of the extra fields it needs (for example `EXTRA_FIELDS = [("weight", "Weight (kg)")]`).
- `FileHandler` would call `PRODUCT_TYPES[item["type"]].from_dict(item)`, and the menu would build its list of choices and its prompts from the registry.

With that in place, adding `SubscriptionProduct` would only mean writing the new class and registering it with one line. None of the existing product-handling code would need to change.
