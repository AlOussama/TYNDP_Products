// ML-C22 research sketch -- NOT PARSER-TESTED / NOT VERIFIED NATIVE SYSML 2.0
// Intended to sketch an external storage role, not to mandate internal SOC variables.
package ResearchStorageContract {
    port def ElectricalInterface;
    part def StorageRole {
        port grid : ElectricalInterface;
    }
    part battery : StorageRole;
    // TODO: use standard RequirementDefinition/Usage, assumedConstraint,
    // requiredConstraint and VerificationCase syntax from the target pilot,
    // then apply a typed profile for carrier/unit/sign/Owner/source/Evidence.
    // This TODO is intentional: prose below is not treated as a passed native test.
}
