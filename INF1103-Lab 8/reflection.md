# INF1103 Lab 8 – Reflection

My Predict First answers, the LSP diagnose answer and my answers for 6.3 and 7.3 are in *Lab 8 Predict First Notes.docx*.

## Design

| Relationship | Classes | In my code | UML |
|---|---|---|---|
| Association | Product → Supplier | The supplier is created first and passed into the Product constructor (`supplier: Supplier`). The product keeps a reference to it but neither one owns the other. | `Supplier 1 —— 0..* Product` |
| Aggregation | Inventory ◇— Product | `self.__products: list[Product]`. Products are made outside and added with `add_product()`. `remove_product()` gives back the same object so it can go into another inventory, and `clear()` only drops the references. | `Inventory 0..1 ◇—— 0..* Product` |
| Composition | Order ◆— OrderLine | Only `Order.add_order_line(product, quantity)` creates order lines. `order_lines` is returned as a tuple so nothing outside can add or move lines. `remove_order_line()` and `cancel()` get rid of them. | `Order 1 ◆—— 0..* OrderLine` |
| Association | OrderLine → Product | An order line refers to a product but does not own it, so the same product can be in many orders and in an inventory. | `OrderLine 0..* —— 1 Product` |
| Inheritance | PhysicalProduct, DigitalProduct → Product | Same as Lab 7, but the supplier is now passed up with `super().__init__()`. | hollow triangle |
| Interface | PhysicalProduct ⋯▷ CanBeShipped | Same as Lab 7. | dashed line, hollow triangle |

`inventory.json` now has a list of suppliers and a list of products. Each product only saves its `supplier_id`, since the supplier is a separate object and not part of the product. When loading, `FileHandler` creates each supplier once and links every product back to that same supplier object.

The menu now asks for a supplier when adding a product, and has new options to remove a product, show suppliers, add a supplier and create an order.

I changed the Docker image from `python:3.9-slim` to `python:3.11-slim` because type hints like `Product | None` need Python 3.10 or newer.

## Type hints

I decided the types in the UML first and then added them to the code:

- References to other objects: `supplier: Supplier`, `product: Product`
- Collections: `list[Product]`, `list[OrderLine]`
- Methods that might not find anything: `find_product(product_id: str) -> Product | None`
- Methods that return nothing: `add_order_line(...) -> None`

I didn't use `Any` anywhere. `TestTypeHints` in `test_lab8.py` reads the hints and checks that they match the diagram. In the UML I wrote the types in a way that isn't Python-specific, for example `Product [0..*]` for a collection and `Product [0..1]` for a product or nothing.

## Testing

`python lab8_demo.py` runs through Sections 2, 3, 4, 6 and 7 and prints the results I used to check my predictions. `python -m unittest -v test_lab8` runs 21 tests covering association, aggregation, composition, type hints, LSP, polymorphism and saving/loading.

## AI use

I used AI to help with the UML diagram and checked each relationship against Section 1. I kept the Supplier link as an association, since a product isn't made up of suppliers. I changed the Inventory end of the aggregation from `0..*` to `0..1`, because in my design a product is only in one inventory at a time and gets moved by removing it from one and adding it to another.

I also used AI to explain some concepts I wasn't sure about in this lab, like the difference between aggregation and composition and why a subclass can break LSP.

## Reflection

My first prediction was wrong. I thought `del supplier` would delete the Supplier object and the products would crash when showing supplier details. It turns out `del` only removes the variable name. The products still had their own references, so the supplier kept existing. The others matched what I expected.

A stored reference doesn't automatically mean aggregation or composition. `Product.supplier` is a reference, but a product isn't made of suppliers, so it's only an association. `OrderLine.product` is the same.

A product can be taken out of an inventory without being destroyed because it is created outside the inventory and still means something by itself. It can be sold, ordered or stored somewhere else. An order line only makes sense inside its order ("2 laptops in order ORD001"). If it got moved to another order, the first order's total would change without anyone noticing, so it makes sense for the order to create it and get rid of it.

Keeping one `list[Product]` in the inventory means it works with any type of product, including new ones added later. Having separate lists for physical and digital products would mean adding a new list, new methods and more `if` checks every time a new type is added.

Type hints make it clear what each attribute holds (a `Supplier` object, not just a supplier name), what is inside a list, and when a method can return `None`, so whoever calls it knows to check. VS Code also picks up some mistakes before the code is run.

The UML would still work for Java or C#. `list[Product]` would just become `List<Product>` and `Product | None` would be a nullable `Product`, but the classes and relationships are the same.

A subclass can inherit from Product and still break LSP. The `DigitalProduct.update_stock()` in the diagnose task that raises `NotImplementedError` is an example. It inherits from Product but breaks code that expects every product to accept a stock update.

## Group project

Our group project is a workplace safety incident triage system. A supervisor logs an incident on a construction site, AI gathers supporting evidence, and fixed rules decide how serious it is before it is saved for review.

- **Association:** Each AI enrichment step (like the hazard flag step and the review step) is given a Gemini client when it is created. The step uses the client but doesn't create or own it, and the same client can be shared between several steps. That fits association.
- **Aggregation:** A photo can be attached to an incident. The photo is created on its own from the uploaded file and then attached, so it exists separately from the incident. Aggregation fits better than composition here.
- **Composition:** The version history of an incident fits composition best. Each snapshot is created by the incident when it is edited, only means something for that one incident, and should be deleted together with it. It should never be moved to a different incident.

If I had to pick one to use more in the project, it would be composition for the incident history. It makes it clear that only the incident is allowed to create and manage its own versions, which stops other parts of the program from changing an incident's past records.
