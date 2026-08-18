# Day-7 B04 Custom ID Schema Note

Day-7 B04 imports `process_id: process:B04_phi_phi_to_h_h` from the locked external knowledge package. The existing PhysicsCard schema previously constrained `process_id` through the same lowercase-only pattern used for local `object_id` values.

The schema now keeps local `object_id` lowercase, but allows `process_id` to use the external ID spelling supplied by audited knowledge packages. Existing B01-B03 IDs remain valid and unchanged.
