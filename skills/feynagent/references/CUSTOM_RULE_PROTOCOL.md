# Custom Rule Protocol

For nonstandard interactions, require:

- explicit Lagrangian term or Feynman rule formula;
- metric, Fourier, momentum-flow, spinor, polarization, and index conventions;
- provenance source and reviewer/audit status;
- particle identities, antiparticles, quantum-field roles, and allowed internal species;
- mapping to FeynCalc elementary objects where practical.

Never invent a trusted rule. If a rule is under-specified, classify the request as `unsupported_requires_review` and ask for the missing rule/convention/provenance only.

Do not silently change channels, signs, conventions, custom rules, masses, gauge choices, or approximation assumptions. Require physics review for such changes.

Preferred implementation target: custom FeynArts-compatible model/adapter. Legacy custom backend is allowed as reference/fallback while the custom native adapter is not available.
