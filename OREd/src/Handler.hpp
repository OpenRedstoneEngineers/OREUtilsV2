/**
 *  ORE Server management daemon
 *  Copyright (C) 2013 OpenRedstone
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef _ORED_HANDLER_
#define _ORED_HANDLER_

#include "Manager.hpp"

namespace OREd
{
	/**
	 * \brief Kick the specified player.
	 */
	bool HandleCmdKick(Client* cli, ConsolePtr& target, const Manager::ArgsList& args);

	/**
	 * \brief Stop the specified server.
	 */
	bool HandleCmdStop(Client* cli, ConsolePtr& target, const Manager::ArgsList& args);

	/**
	 * \brief (Re)start the specified server.
	 */
	bool HandleCmdStart(Client* cli, ConsolePtr& target, const Manager::ArgsList& args);

	/**
	 * \brief Kill the specified server.
	 */
	bool HandleCmdKill(Client* cli, ConsolePtr& target, const Manager::ArgsList& args);
} /* OREd */

#endif
