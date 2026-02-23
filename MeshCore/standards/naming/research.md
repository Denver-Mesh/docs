### MeshCore Naming Convention:

##### Ref:
	- https://wiki.meshcoreaus.org/books/ent-naming/page/ent-node-names
	- https://nswmesh.au/docs/meshcore/sydney-meshcore.html
	- https://analyzer.letsmesh.net/nodes/prefix-utilization
	- https://gessaman.com/mc-keygen/

#### Repeaters

##### Name

The name of a given repeater/room server will be visible and potentially saved into contacts for all companions on the mesh.

Names are capped at 23 characters.

The following are different ideologies and designs around standardized naming schemes:
###### Location-Based

As [followed by the New South Wales, Australia mesh](https://nswmesh.au/docs/meshcore/sydney-meshcore.html), nodes are simply named by a nearby location, such as a suburb, a crossroads or a landmark. For example, a repeater on top of Lookout Hill might be called "Lookout Hill Repeater". When using roads, names should be named after specific crossroads/intersections, as many roads can stretch for miles in various directions.

Names should be suffixed with the node type (e.g. `Repeater`, `Room`).

If multiple nodes of the same type exist in the same landmark, you may consider suffixing with additional information, such as a number (e.g. `1`, `2`) or some other location identifier (e.g. `Tree`, `Ground`, `Flagpole`)

Given that names are capped at a maximum 23 characters, it is recommended to use common abbreviations where appropriate. Node types can be abbreviated (`Rpt` for "repeater", `Rm` for "room"). These node abbreviations should be reserved when possible (do not abbreviate other words to produce the same abbreviation as `Rpt` or `Rm`)

Separator characters like spaces (` `) and dashes (`-`) should be used sparingly. The name `LookoutMtnRpt1` conveys the same information in less characters than `Lookout Mountain Repeater 1`.

###### Short-Code-Based

As [followed by other meshes in Australia](https://wiki.meshcoreaus.org/books/ent-naming/page/ent-node-names), nodes are named with a sequence of codes that, when combined, given information on its location and type.

This pattern may vary based on country, as will require coordination between mesh members to agree upon codes.

The format `[SSS3]-[LOC12]-[TYPE3]-[ID2]` is as follows:
- `[SSS3]`: An uppercase, <=3-character code representing the state/province/territory
	- `CO` for Colorado, U.S.
	- `BC` for British Colombia, Canada
	- `VIC` for Victoria, Australia
- `[LOC12]`: An uppercase, <=12-character code representing a more specific location, such as a city or a prominent landmark
	-  `DENVER` for Denver, Colorado, U.S. 
	- `PIKESPEAK` for Pikes Peak Mountain in Colorado, U.S.
	- `SEARSTOWER` for Sears Tower, Chicago, U.S.
- `[TYPE3]`: An uppercase, 3-character code representing the type of node. The types and abbreviations will need to be agreed upon by the mesh community.
	- Australia uses the following types, which relate to the power/role of a given node in the mesh infrastructure:
		1. `COR` = **Core**: Long backbone links to join smaller distribution areas together with less hops. High elevation mountain-top/tower mounted nodes in remote locations. Independently powered (i.e. not grid-tied) with battery backup. May use directional or omnidirectional antennas. Companion nodes typically would not connect directly to a _core_ node.
		2. `DIS` = **Distribution**: Mid to long range links with reliable connectivity to at least one _core_ node and ideally multiple other _distribution_ nodes to provide path redundancy. Typically at a high elevation point within a suburban area and used to join _edge_ repeaters to the wider mesh. Independently powered (i.e. not grid-tied) with battery backup. Should only use omnidirectional antennas. Not to be used for rooftop/residential nodes.
		3. `EDG` = **Edge**: Rooftop and residential nodes. Any elevation OK. Reliability not a strict requirement. Mains power acceptable.
		4. `MOB` = **Mobile**: Vehicle-mounted, on-person carried, and temporary nodes. Wild west; anything goes.
	- Others may decide to have types that relate to MeshCore firmware types:
		- `RPT` = Repeater
		- `ROM` = Room (*For consistency and machine parsing, it is best to keep all these abbreviations EXACTLY 3 characters*)
		- `COM`= Companion
- `[ID2]`: A 2-character code identifying the node. These **can be** decided by the node owner, especially for companion devices, but to avoid potential common duplicates (e.g. `A1` and `A2`), it is recommended to use the first two characters of a unique public key (see [[#Public Key (ID)]])

CLARIFICATION: The `[ ]` characters are simply placeholders for the format, and would NOT appear in the final name.

For a repeater node mounted on Pikes Peak in Colorado, U.S., the name could be `CO-PIKESPEAK-RPT-XX`, where `XX` represents the first two characters of its public key (e.g. `F4`)

For a room node in Atlanta, Georgia, the name could be `GA-ATL-ROM-XX`, where `XX` represents the first two characters of its public key (e.g. `F4`). While spelling out `ATLANTA` would still keep the node name below 23 characters, this demonstrates that, especially for longer city names, well-known abbreviations can help save space.

Since Atlanta is a big city that it certain to have more than one room node in it, the owner could be more specific with the locality. For example, a specific suburb or neighborhood of Atlanta, such as Inman Park. The name `GA-INMANPARK-ROM-XX` is more specific to the nodes exact location.

A variation of this format, particularly for large countries like the United States where traffic is likely not leaving a given state, is to replace the state/province/territory with a city abbreviation, and replace the locality with a landmark or crossroads/intersection. For example, in the Inman Park, Atlanta example, we assume the node is going to be in Georgia, so instead name the node `INM-MORELAND-ROM-XX`, where the `INM` stands for Inman Park and `MORELAND` represents Moreland Avenue, a well-known road in the neighborhood.

For nodes near state borders, where representing the state in the name makes more sense, the first format is more applicable.

###### Owner-Based

In the event where identifying *who* is operating a node is more important than knowing where the node is, nodes can be named after the owner (with additional optional metadata such as location or IDs).

There are multiple ways to approach this scheme, many of which involve community agreement upon a standard approach:

- The name of a given node would partially or entirely include the name of the node's owner and/or primary operator (such as the business hosting the node). Names should remain under the 23-character limit. Collisions with this naming approach are unlikely.
- Licensed ham radio operators may choose to include their callsign in the node name to link it to them and their ham identity.
- A community may choose to keep a ledger of their own assigned and/or reserved identifiers, such as unique callsigns or emojis, and the corresponding individuals.

One consideration for this approach is regarding location. While details about a given node's location may not be immediately identifiable through its name, most physical nodes (typically repeaters/rooms automatically, and companions by user choice) include their GPS or fixed location in their adverts. The location of a node is therefore usually already available in the MeshCore client apps and displayable on a map, meaning there is no need to waste space in the node's name to convey that information. This also removes the requirement of keeping the node's "name location" in sync with its actual physical GPS location.

At the same time, this approach can reveal information some node operators might otherwise wish to keep private. Some ham operators may not wish to utilize their callsign, which, through a simple lookup in a publicly-available database, could link a given node to the operator's real name and address. Because nodes communicate their location with often medium-to-high accuracy, a malicious actor could easily connect the dots that, e.g. a "John Smith" repeater node that is always adverting from a specific residential address signifies that John Smith lives at that address.

###### Our Proposal

**The following is subject to change as MeshCore evolves and more meshes take shape and grow.**

**NOTE: This proposal is designed with primarily the United States in mind, and may not be entirely applicable to other countries.**

We recommend a hybrid approach, using the [[#Short-Code-Based]] approach as a base.

`[STATE 2/3]-[CITY 7]-[LANDMARK 7]-[TYPE + ROLE 2][COUNTER 2]`

Regex pattern: `[A-Z0-9]{2,3}\-[A-Z0-9]{1,7}\-[A-Z0-9]{1,7}\-[C,T,TR,TM,RC,RD,RE,RM][0-9][0-9]`

Example: `CO-DENVER-CHSPARK-RC01` would represent the first core repeater, located in Cheesman Park in Denver, Colorado.

The various components of the code are as follows:
	1. `[STATE 2/3]`: This is the [2- or 3-character alpha abbreviation](https://en.wikipedia.org/wiki/List_of_U.S._state_and_territory_abbreviations) for the state (or province/territory) where the node is located. While it is unlikely users will interact with nodes outside of their current state, this helps with identifying nodes nationally and internationally on online maps. For smaller countries without prominent subdivisions, the 2- or 3-character variant of the country's [ISO-3166-1 code](https://en.wikipedia.org/wiki/ISO_3166-1) can be used instead.
	2. `[CITY 7]`: This is a <=7-character abbreviation of the city or region inside the state/province/territory where the node is located. This and `[LANDMARK 7]` will likely be the hardest part of the code, as space is limited and there are less agreed-upon standard codes here. Abbreviations should be reasonable, and with the understanding that this block may represent a city, filler words can be cut. Community members may choose to establish standards for common city/region names.
	3. `[LANDMARK 7]`: This is a <=7-character abbreviation of a landmark nearby where the node is located. This may include street intersections or other physical markers. The goal of this block is to give a rough idea of where the node is physically located in the event of maintenance. Exact location is not always required and can be exaggerated for privacy purposes.
		- For instances where the landmark is prominent enough that the city is irrelevant (e.g. on a specific mountain peak), the `[CITY 7]` block can be dropped entirely and the extra space reallocated to the `[LANDMARK 7]` block.
		- It is important to remember that many nodes will broadcast their GPS location, which any mesh user can see and use to find the node. This name block does not need to be hyper-specific; it is merely to indicate where approximately in the city/region the node is located.
	4. `[TYPE + ROLE 2]`: This is a 1- or 2-character abbreviation signifying the firmware type and (optionally) infrastructure role of a given node. The following options are available:
		- `T`: The node is a static (non-mobile) room server, flashed with the Room Server firmware. This node's location does not change.
		- `TM`: The node is a mobile (non-static) room server, flashed with the Room Server firmware. This node's location changes often or is inconsistent.
		- `TR`: This node is a room server, flashed with the Room Server firmware, with `set repeat on` enabled to act as a semi-repeater. The static vs. mobile nature of this node is not indicated.
		- `RC`: This node is a repeater, flashed with the Repeater firmware, and is considered a "core" or "critical" repeater. This node receives high traffic and/or is a vital backbone in the mesh.
		- `RD`: This node is a repeater, flashed with the Repeater firmware, and is considered a "distributed" repeater. This node bridges (likely a single) core repeater with (multiple) edge repeaters.
		- `RE`: This node is a repeater, flashed with the Repeater firmware, and is considered an "edge" repeater. This node connects a small area, from a single building to an entire neighborhood, to a distributed repeater.
		- `RM`: This node is a mobile (non-static) repeater, flashed with the Repeater firmware. This node's location changes often or is inconsistent.
	5. `[COUNTER 2]`: A 2-digit counter to identify separate physical devices that serve the same type/role in the same general location. This counter should start at `01` and continue to `99`. Community members will need to coordinate to avoid duplicate counters, although it is unlikely that multiple nodes, of the same type and at the same city + landmark combination, are not already operated by the same owner.

With hyphens included and each block maxed out, the name will reach its maximum 23-character limit. It is vital that each section respect its character limit.
##### Public Key (ID)

Each repeater/room server on the mesh is identified by the first two characters of its public key. If two nodes have the same first two characters (e.g. `aa`), it is virtually impossible to tell if a given node is, e.g. `aa01` or `aa56`.

To avoid collisions with other repeaters/room servers, please set a public key for your node that starts with a unique 2-character prefix.

A list of all claimed and unclaimed prefixes is available here: https://analyzer.letsmesh.net/nodes/prefix-utilization

Simply click an unclaimed prefix (green block) to open https://gessaman.com/mc-keygen/ and generate a public key beginning with that prefix.

This does NOT compromise the security of your node. These are public keys, intended by design to be shared. Nevertheless, key calculations on the keygen website are done entirely locally and never transmitted to a server.

#### Companions

Community coordination is highly encouraged for repeaters (i.e. physical location, naming scheme). Companions (clients), on the other hand, are always going to be more driven by the owner's personal preference. It is foolish to attempt to standardize companion node naming.

Some notes and recommendations:
- All companions belonging to the same owner should start with the same prefix, with a suffix that is either a counter (`01`, `02`) or the first 2 characters of the node's public key.
- Community members may wish to assign callsigns or emoji prefixes so that users can easily "look up" an advertised node and find its associated owner in a shared directory. The opposite approach also works; if Alice knows Bob's nodes are prefixed with `🐿️` and suffixed with a counter, Alice can look up `🐿️ 01` to find Bob's first companion node and attempt to contact him.
- Companion names should NOT contain information about the physical device. As an end-user, Bob likely doesn't care if someone reaches him on my T-Deck or his Heltec v4. But he does care if someone reaches him on `🐿️ 01` (the node he is taking with him on a trip) rather than `🐿️ 02` (the node he is leaving behind at home). By keeping the node name hardware-agnostic, Bob has the option to swap node names between his physical devices (e.g. the T-Deck `🐿️ 01` becomes `🐿️ 02`, and the Heltec v4 `🐿️ 02` becomes `🐿️ 01`) without having to inform his contacts to send messages to a different target.
	- You can think about each companion node as a different email address, each belonging to the same person. It doesn't matter whether the email message is read on a laptop versus a phone, just so long as it reaches the right inbox!
