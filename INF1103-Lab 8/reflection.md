# INF1103 Lab 8 – Notes & Reflection

The "Predict first" answers, the LSP "Diagnose" answer and the Section 6.3 / 7.3 explanations are in **Lab 8 Predict First Notes.docx**.

## Design summary

| Relationship | Classes | How it shows in the code | UML |
|---|---|---|---|
| **Association** (knows-about) | `Product` → `Supplier` | The Supplier is created first and passed into `Product.__init__(..., supplier: Supplier)`. Product stores the reference (`self.__supplier: Supplier`). Neither creates nor owns the other. | `Supplier 1 —— 0..* Product` |
| **Aggregation** (has-a, parts independent) | `Inventory` ◇— `Product` | `self.__products: list[Product]`. Products are created outside and passed to `add_product()`. `remove_product()` returns the same object, so it can be added to another Inventory. `clear()` only drops references. | `Inventory 0..1 ◇—— 0..* Product` |
| **Composition** (owns, lifecycle tied) | `Order` ◆— `OrderLine` | Only `Order.add_order_line(product, quantity)` creates `OrderLine` objects. `order_lines` is returned as a read-only tuple, so lines cannot be added or moved from outside. `remove_order_line()` and `cancel()` discard them. | `Order 1 ◆—— 0..* OrderLine` |
| **Association** | `OrderLine` → `Product` | OrderLine refers to a Product but does not own it. The same Product can be in many orders and in an Inventory. | `OrderLine 0..* —— 1 Product` |
| **Inheritance** | `PhysicalProduct`, `DigitalProduct` → `Product` | From Lab 7, now passing `supplier` up through `super().__init__()`. | hollow triangle |
| **Interface** | `PhysicalProduct` ⋯▷ `CanBeShipped` | From Lab 7. | dashed, hollow triangle |

**Persistence:** `inventory.json` now has a `suppliers` list and a `products` list. Each product only saves its `supplier_id` (the Supplier is a separate object, not part of the product). On loading, `FileHandler` builds each Supplier once and links every product back to that **same** Supplier object.

**Menu integration:** `inventory_manager.py` now asks for a supplier when adding a product and has new options for *Remove Product*, *Display Suppliers*, *Add Supplier* and *Create Order*.

**Docker:** the base image moved from `python:3.9-slim` to `python:3.11-slim`, because type hints like `Product | None` need Python 3.10 or newer.

## Type hints (Section 5)

Every attribute, parameter and return value has a type hint, chosen from the design first and then written in code. Examples:

- Object references: `supplier: Supplier`, `product: Product`
- Collections: `list[Product]`, `list[OrderLine]` (and `tuple[OrderLine, ...]` for the read-only view)
- Optional results: `find_product(product_id: str) -> Product | None`, `remove_product(product_id: str) -> Product | None`
- No result: `add_order_line(...) -> None`, `display_information() -> None`
- `Any` is not used anywhere.

`from __future__ import annotations` is used so the hints are not evaluated while the module loads. `TestTypeHints` in `test_lab8.py` reads the hints with `typing.get_type_hints()` and checks they match the UML.

In the UML diagram the types are written in a language-independent way: `Product [0..*]` for a collection and `Product [0..1]` for "a Product or nothing".

## Testing (Section 9)

- `python lab8_demo.py`: walks through Sections 2, 3, 4, 6 and 7 and prints the results used to check each Predict First answer.
- `python -m unittest -v test_lab8`: 21 tests covering association, aggregation, composition, type hints, LSP, polymorphism and JSON persistence.

## AI use (Section 8)

I used an AI assistant to help draft the UML diagram and checked every relationship it chose against Section 1.

- **Accepted:** `supplier: Supplier` drawn as a plain **association** (solid line, arrow towards Supplier) and not as aggregation, because a Product is not a whole made of Suppliers, and `OrderLine → Product` also as an association, because an OrderLine refers to a Product but does not own it.
- **Changed:** the multiplicity at the Inventory end of the aggregation. The draft had `0..*` (a product can be shared by many inventories). I changed it to `0..1` because in my design a product is in at most one inventory at a time and is *moved* by removing it from one and adding it to another.

## Optional reflection (Section 10)

**Can an object reference exist without being aggregation or composition?**
Yes. `Product.supplier` is a stored reference, but a Product is not made of Suppliers, so it is only an association. The same is true for `OrderLine.product`.

**Why can a Product be removed from an Inventory without being destroyed, while an OrderLine belongs to an Order?**
A Product is created outside the Inventory and has a meaning by itself (it can be sold, ordered, or stored somewhere else). An OrderLine only means something as part of its Order ("2 laptops *in order ORD001*"). If it were moved to another Order, the first order's total would silently change, so the Order creates it and it ends with the Order.

**Why should Inventory store Product references rather than separate collections for each subclass?**
One `list[Product]` lets the Inventory work with any current or future subclass without changing. Separate lists would need a new list, new methods and new `if` checks each time a product type is added, which breaks the Open/Closed Principle.

**How do type hints communicate design decisions?**
They show at a glance what an attribute holds (`Supplier`, not a supplier name string), what a collection contains, and when a method may return nothing (`Product | None`), so the caller knows to check for `None`. The IDE can also warn about wrong types before the program runs.

**Would the UML design still make sense in Java or C#?**
Yes. The diagram uses UML types and multiplicities (`Product [0..*]`, `Product [0..1]`) rather than Python syntax. In Java, `list[Product]` would become `List<Product>` and `Product | None` would be a nullable `Product` or `Optional<Product>`, but the classes and relationships stay the same.

**Can a subclass inherit from Product but still violate LSP?**
Yes. The `DigitalProduct.update_stock()` that raises `NotImplementedError` in the Diagnose task inherits from Product but breaks the promise that `update_stock()` works for every Product, so code written for Product crashes.

**Where could the group project use these relationships?** *(edit this to match your project)*
A main application object that creates its own manager objects and is the only thing that uses them would be **composition**, because the managers are created by, and end with, the application. Objects that are passed in from outside and only used (for example a shared configuration or data object) would be **association**.
